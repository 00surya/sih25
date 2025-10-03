import uuid 
from app import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  
    last_login_date = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)


    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

