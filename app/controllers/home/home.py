# controllers/main_controller.py
from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

home_bp = Blueprint('home', __name__)

# --------------------------
# Home Page
# --------------------------
@home_bp.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    if not current_user:
        return redirect(url_for('login.login_page'))

    return render_template('home/home.html')

