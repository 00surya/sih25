from app import db
from datetime import datetime
from app.utils.time_formatter import FormatTime
import uuid


class Draft(db.Model):
    __tablename__ = "draft"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    draft_file = db.Column(db.String(60), nullable=False)
    result_file = db.Column(db.String(60), nullable=True)  # new
    processing = db.Column(db.Boolean, default=True)  # new
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    user = db.relationship("User", backref="draft")
    # processed_comments = db.relationship("ProcessedComment", backref="draft", lazy=True)



    def to_dict(self):

        date = FormatTime.format_time(self.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        edited = False
        if self.updated_at:
            date = FormatTime.format_time(self.updated_at.strftime("%Y-%m-%d %H:%M:%S"))
            edited = True

        data = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "desc": self.desc,
            "created_at": self.created_at,
            "updated_at": self.updated_at if self.updated_at else None,
            "date": date,
            "edited": edited,
            "processing":self.processing
        }


        return data
