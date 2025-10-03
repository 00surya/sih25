from app import db
from datetime import datetime as dt
from app.utils.time_formatter import FormatTime
import uuid


class ProcessedComment(db.Model):
    __tablename__ = 'processed_comments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    draft_id = db.Column(db.String(36), db.ForeignKey('draft.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    sentiment_label = db.Column(db.String(20))
    sentiment_score = db.Column(db.Float)
    section = db.Column(db.String(100))       # Optional
    article = db.Column(db.String(100))       # Optional
    chapter = db.Column(db.String(100))       # Optional
    datetime = db.Column(db.DateTime)    # Optional
    comment_datetime = db.Column(db.DateTime)    # Optional
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=dt.utcnow)