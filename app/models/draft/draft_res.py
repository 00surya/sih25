from app import db
from datetime import datetime
import uuid


class ProcessedResults(db.Model):
    __tablename__ = 'processed_results'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    draft_id = db.Column(db.String(255), nullable=False, unique=True)  # Associate with draft_id
    results = db.Column(db.JSON, nullable=False)  # Store processed results in JSON format
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of when it was processed

    def __init__(self, draft_id, results):
        self.draft_id = draft_id
        self.results = results
