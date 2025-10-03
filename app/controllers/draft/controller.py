# app/controllers/auth/login.py

from flask import Blueprint, request, redirect, url_for
from app.services.draft.draft_service import DraftService
from app.utils.response import error_response
from flask_jwt_extended import jwt_required, get_jwt_identity


draft_bp = Blueprint('draft', __name__, url_prefix='/u/draft')

@draft_bp.route('/api/add', methods=['POST'])
@jwt_required(optional=True)
def draft_add_api():
    current_user = get_jwt_identity()
    print(current_user)

    if not current_user:
        return redirect(url_for('login.login_page'))

    data = request.get_json()

    if not data:
        return error_response("No JSON payload provided.", 400)

    title = data.get('title')
    desc = data.get('description')
    file_url = data.get('csv_url')

    if not title or not desc or not file_url:
        return error_response("All fields are required.", 400)

    return DraftService.add_draft(title=title, desc=desc, file_url=file_url, user_id = current_user)


@draft_bp.route("/list", methods=["GET"])
@jwt_required()
def get_drafts():

    current_user = get_jwt_identity()  
    if not current_user:
        return redirect(url_for('login.login_page'))
    
    return DraftService.draft_list(user_id=current_user)
