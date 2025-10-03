import io
import csv
from datetime import datetime
from app import db
from app.models.draft.draft import Draft
from app.services.summarize.t5 import T5Summary
from app.services.aws_clients import s3_client
from app.config.aws_config import S3_BUCKET
# Import the new dashboard service
from app.services.dashboard.dashboard_service import generate_and_save_dashboard_data

# Initialize summarizer
summarizer = T5Summary()

def process_draft(draft_id=None, file_key=None, batch_size=15, adaptive_batch=True):
    """
    Process a draft CSV for summarization + sentiment.
    Can be called with either draft_id OR file_key.
    """
    draft = None
    print("in draft", draft_id)

    draft = Draft.query.filter_by(id=draft_id).first()

    if not draft:
        print(f"[ERROR]: Draft {draft_id} not found")
        return
    file_key = f"uploads/{draft.draft_file}"

    print(f"[INFO]: Processing draft: {draft.title} ({draft.id})")

    # 1. Download file from S3
    try:
        obj = s3_client.get_object(Bucket=S3_BUCKET, Key=file_key)
        content = obj['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"[ERROR]: Failed to download file {file_key}: {e}")
        return

    # 2. Parse CSV
    reader = csv.DictReader(io.StringIO(content))
    fieldnames = reader.fieldnames

    # Case-insensitive check for comment column
    comment_col = None
    if fieldnames:
        for col in fieldnames:
            if col.lower() == "comment":
                comment_col = col
                break

    if not comment_col:
        print("[WARNING]: 'comment' column not found")
        return

    data_rows = list(reader)
    if not data_rows:
        print("[WARNING]: CSV is empty")
        return

    # Add new columns
    summary_column = "comment_summary"
    sentiment_column = "comment_sentiment"
    new_fieldnames = fieldnames + [summary_column, sentiment_column]

    total_rows = len(data_rows)
    if adaptive_batch and total_rows < batch_size:
        batch_size = 1
    total_batches = (total_rows + batch_size - 1) // batch_size
    processed_rows = []

    # 3. Process in batches
    for i in range(0, total_rows, batch_size):
        batch = data_rows[i:i + batch_size]
        comments = [row.get(comment_col, "") for row in batch]

        batch_number = (i // batch_size) + 1
        print(f"[INFO]: Processing batch {batch_number}/{total_batches} ({len(comments)} comments)")

        try:
            results = summarizer.summarize_with_sentiment(comments)

            if len(results) != len(batch):
                print(f"[WARNING]: Results mismatch: got {len(results)} results for {len(batch)} rows")
                results.extend([{"summary": "ERROR", "sentiment": {"label": "ERROR", "score": 0}}] * (len(batch) - len(results)))

            for row, res in zip(batch, results):
                row[summary_column] = res.get("summary", "")
                sentiment = res.get("sentiment", {"label": "UNKNOWN", "score": 0})
                row[sentiment_column] = f"{sentiment['label']} ({sentiment['score']:.2f})"
                processed_rows.append(row)

        except Exception as e:
            print(f"[ERROR]: Batch {batch_number} failed: {e}")
            for row in batch:
                row[summary_column] = "ERROR"
                row[sentiment_column] = "ERROR (0.0)"
                processed_rows.append(row)

    print(f"[DEBUG]: Processed {len(processed_rows)} rows total")

    # 4. Write CSV
    output_buffer = io.StringIO()
    writer = csv.DictWriter(output_buffer, fieldnames=new_fieldnames)
    writer.writeheader()
    writer.writerows(processed_rows)
    csv_content = output_buffer.getvalue()

    # 5. Upload results to S3
    result_key = f"results/{draft.draft_file}"
    try:
        s3_client.put_object(Bucket=S3_BUCKET, Key=result_key, Body=csv_content.encode("utf-8"))
        print(f"[SUCCESS]: Results CSV uploaded to {result_key}")
    except Exception as e:
        print(f"[ERROR]: Failed to upload results CSV: {e}")
        return

    # 6. ✨ NEW: Generate and save dashboard data
    try:
        generate_and_save_dashboard_data(draft_id, csv_content)
    except Exception as e:
        # Log the error, but don't stop the process since the main CSV is already saved.
        print(f"[ERROR]: Dashboard data generation failed for {draft_id}: {e}")


    # 7. Update draft in DB
    try:
        draft.result_file = result_key
        draft.processing = False
        draft.updated_at = datetime.utcnow()
        db.session.commit()
        print(f"[INFO]: Draft {draft.id} status updated successfully.")
    except Exception as e:
        print(f"[ERROR]: Failed to update draft status in DB: {e}")
