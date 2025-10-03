import os
import uuid
from werkzeug.utils import secure_filename

# Allowed extensions for file upload
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def is_allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Secure and make filename unique using UUID."""
    filename = secure_filename(filename)
    extension = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex}{extension}"
    return unique_name

def get_file_extension(filename):
    """Return file extension (lowercase)."""
    return os.path.splitext(filename)[1].lower()

def get_file_size(file_obj):
    """Return file size in bytes."""
    file_obj.seek(0, os.SEEK_END)
    size = file_obj.tell()
    file_obj.seek(0)  # Reset pointer
    return size

def is_file_size_valid(file_obj, max_size=MAX_FILE_SIZE):
    return get_file_size(file_obj) <= max_size
