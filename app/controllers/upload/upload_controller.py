from flask import Blueprint, request
from werkzeug.utils import secure_filename
from app.services.upload.s3_service import upload_file_to_s3
from app.utils.response import success_response, error_response
from app.utils.file_helpers import is_allowed_file, generate_unique_filename, is_file_size_valid
from app.config.aws_config import QUEUE_URL
import json
from app.services.aws_clients import sqs_client

# Use sqs_client.send_message(...)


upload_bp = Blueprint('upload', __name__, url_prefix='/upload')
@upload_bp.route('/csv', methods=['POST'])
def upload():

    file = request.files.get('file')
    if not file:
        return error_response("No file uploaded")

    if not is_allowed_file(file.filename):
        return error_response("File type not allowed", 400)

    if not is_file_size_valid(file):
        return error_response("File size exceeds 10MB limit", 413)

    filename = generate_unique_filename(file.filename)

    try:
        upload_file_to_s3(file, filename)
    
        # Send SQS message with file key so worker can pick it up
        # message_body = json.dumps({"file_key": filename})
        # sqs_client.send_message(QueueUrl=QUEUE_URL, MessageBody=message_body)
        
        return success_response({"url": filename}, "File uploaded successfully")
    except Exception as e:
        return error_response(f"Upload failed: {str(e)}", 500)
