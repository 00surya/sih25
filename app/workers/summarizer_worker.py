import time
import json
import boto3

from app import create_app  # <-- make sure you have this
from app.services.summarize.summarizer_service import process_draft
from app.config.aws_config import QUEUE_URL
from app.services.aws_clients import sqs_client

app = create_app()  # creates and configures your Flask app

def start_worker():
    print("📡 Worker started. Listening to SQS...")

    while True:
        response = sqs_client.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20  # long polling
        )

        messages = response.get('Messages', [])

        if not messages:
            continue  # No messages, poll again

        for msg in messages:
            try:
                body = json.loads(msg['Body'])
                file_key = body['file_key']
                print(f"Received job for draft: {file_key}")
    
                # 💡 Push the Flask app context so Flask internals can be used
                with app.app_context():
                    process_draft(draft_id=file_key)

                # Delete message after success
                sqs_client.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=msg['ReceiptHandle']
                )
                print("✅ Job completed and message deleted.")

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                # optionally send to Dead Letter Queue

        time.sleep(1)

if __name__ == "__main__":
    start_worker()
