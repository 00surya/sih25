# controllers/main_controller.py
from flask import Blueprint, render_template, request, jsonify
from app.services.auth.register import Register 
from app.utils.response import error_response
# from app.services.summarize.job_service import JobService

register_bp = Blueprint('register', __name__, url_prefix='/auth/register')


@register_bp.route('/')
def register_home():
    return render_template('auth/register.html')

@register_bp.route('/api/register', methods=['POST'])
def register_api():
    """
    Handles user registration by creating a new User record in the database.
    Expects a JSON payload with 'name', 'email', and 'password'.
    """
    # 1. Get the JSON data from the request body
    data = request.get_json()
    if not data:
        # return jsonify({"error": "Invalid request: No JSON payload received."}), 400
        return error_response("Invalid request: No JSON payload received.", 400)

    # Match the fields from your User model
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return error_response("Password must be same.", 400)


    # 2. Validate the input fields
    if not all([name, email, password]):
        # return jsonify({"error": "Missing required fields: name, email, and password are all required."}), 400
        return error_response("Missing required fields: name, email, and password are all required.", 400)
        

    return Register.put_user(name=name, email=email, password=password)
   