import os
from flask import Flask
# from app.extensions import db, migrate, jwt, csrf, socketio
# from app.extensions import csrf
# from app.extensions import jwt
# from config import Config


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)

    # Initialize extensions once
    # db.init_app(app)
    # migrate.init_app(app, db)
    # jwt.init_app(app)
    # csrf.init_app(app)



    
    
    # Ensure upload folder exists
    # os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Middleware
    # from app.middleware.auth_middleware import handle_token_refresh, inject_user
    # from app.middleware.error_middleware import register_error_handlers
    # from app.middleware.security_middleware import add_security_headers
    # from app.middleware.logging_middleware import configure_logging
    # from app.middleware.rate_limiting_middleware import configure_rate_limiting
    # from app.middleware.session_middleware import manage_session_expiration

    # app.before_request(handle_token_refresh)
    # app.context_processor(inject_user)
    # app.after_request(add_security_headers)
    # register_error_handlers(app)
    # configure_logging(app)
    # configure_rate_limiting(app)
    # app.before_request(manage_session_expiration)

    # OAuth setup
    # from flask_dance.contrib.google import make_google_blueprint
    # from flask_dance.contrib.github import make_github_blueprint

    # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # google_oauth_bp = make_google_blueprint(
    #     client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    #     client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    #     scope=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
    #     redirect_to='google_login'
    # )
    # github_oauth_bp = make_github_blueprint(
    #     client_id=app.config['GITHUB_OAUTH_CLIENT_ID'],
    #     client_secret=app.config['GITHUB_OAUTH_CLIENT_SECRET'],
    #     scope='user:email',
    #     redirect_to='github_login'
    # )
    # app.register_blueprint(google_oauth_bp, url_prefix='/google_login')
    # app.register_blueprint(github_oauth_bp, url_prefix='/github_login')

    # Import models (registers with SQLAlchemy)
    # from app import models

    # Register blueprints
    from app.controllers.home.home import home_bp
    from app.controllers.summary.controller import summary_bp


    app.register_blueprint(home_bp)
    app.register_blueprint(summary_bp)
    

    # Socket.IO setup
    # from app.socket import register_socket_handlers
    # socketio.init_app(app)  
    # register_socket_handlers()

    # with app.app_context():
    #     db.create_all()

    return app
