from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
# from flask_wtf import CSRFProtect
# from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
# csrf = CSRFProtect()
# socketio = SocketIO(cors_allowed_origins="*")



