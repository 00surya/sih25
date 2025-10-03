import os
from datetime import timedelta
class Config:


    # Secret key for Flask app (used for sessions and forms)
    SECRET_KEY = 'dsdd3e2ew2d23d3'

    # Database URI
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:pop090#nkK@127.0.0.1:3306/lokniti'

    # Disable SQLAlchemy track modifications (optional performance improvement)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    JWT_SECRET_KEY = 'dskdnkdkwndkwndnwd'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'Pl$0T1.s_2.K1J9.apW_'
    JWT_REFRESH_COOKIE_NAME = 'x9fT7s2K1^J9.fd$c36E'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False # False for localhost only (where use http)
    JWT_COOKIE_SAMESITE = 'Lax' # Use Lax on localhost otherwise Strict
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  
    
    
    # Enable JWT CSRF protection
    JWT_COOKIE_CSRF_PROTECT = True