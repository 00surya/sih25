import os
from flask import Flask

from app.extensions import db, migrate
# from app.extensions import csrf
from app.extensions import jwt
from app.config.app_config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions once
    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)
    # csrf.init_app(app)


    # Import models (registers with SQLAlchemy)
    from app import models

    # Register blueprints
    from app.controllers.home.home import home_bp
    from app.controllers.summary.controller import summary_bp
    from app.controllers.upload.upload_controller import upload_bp
    from app.controllers.auth.login import login_bp
    from app.controllers.auth.register import register_bp
    from app.controllers.draft.controller import draft_bp
    from app.controllers.dashboard.controller import dashboard_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(draft_bp)
    app.register_blueprint(dashboard_bp)
    

    # Socket.IO setup
    # from app.socket import register_socket_handlers
    # socketio.init_app(app)  
    # register_socket_handlers()

    with app.app_context():
        db.create_all()

    return app
