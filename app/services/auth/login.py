# app/services/auth/login.py

from app.models.user.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import jsonify, make_response
from app.utils.response import success_response, error_response

class LoginService:
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return error_response("Invalid email or password.", 401)

        access_token = create_access_token(identity=user.id)

        response = make_response(success_response(
            message="Login successful!",
            status_code=200,
            data={
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        ))

        set_access_cookies(response, access_token)
        return response
