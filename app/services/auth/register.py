from app.models.user.user import User
from app.extensions import db
from flask import Blueprint, render_template, request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies

from app.utils.response import error_response, success_response

class Register():
    '''
    - name = user name
    - user_give_id = email or phone which ever user given
    - password = user  account password
    - email = is email true put the user_give_id in email else put it in the number.
    '''
    @staticmethod
    def put_user(name, email, password):

        if User.query.filter_by(email=email).first():
            return error_response(f"A user with the email '{email}' already exists.", 409)


        new_user = User(
            name=name,
            email=email
        )
         
        new_user.set_password(password)


        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}") 
            # return jsonify({"error": "Failed to register user due to a database error."}), 500
            return error_response(f"Failed to register user due to a database error.", 500)
        
        

        user_d = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }

        # 1. Generate access token
        access_token = create_access_token(identity=new_user.id)

        # 2. Create response object with the JSON response
        response = make_response(success_response(
            message="User registered successfully!",
            status_code=201
        ))

        # 3. Set the JWT as an HTTP-only cookie
        set_access_cookies(response, access_token)

        return response