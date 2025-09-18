# controllers/main_controller.py
from flask import Blueprint
# from flask_jwt_extended import jwt_required

home_bp = Blueprint('home', __name__)

# --------------------------
# Home Page
# --------------------------
@home_bp.route('/')
# @jwt_required(optional=True)
def home():
    return "SIH'25 Home page"

