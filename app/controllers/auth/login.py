# app/controllers/auth/login.py

from flask import Blueprint, request, render_template
from app.services.auth.login import LoginService
from app.utils.response import error_response

login_bp = Blueprint('login', __name__, url_prefix='/auth/login')

@login_bp.route('/')
def login_page():
    return render_template('auth/login.html')


@login_bp.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()

    if not data:
        return error_response("No JSON payload provided.", 400)

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return error_response("Email and password are required.", 400)

    return LoginService.login_user(email=email, password=password)
