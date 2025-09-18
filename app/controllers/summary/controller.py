# controllers/main_controller.py
from flask import Blueprint, render_template, request, jsonify
from app.services.summarize.t5 import T5Summary
# from flask_jwt_extended import jwt_required

summary_bp = Blueprint('summary', __name__, url_prefix='/summary')

@summary_bp.route('/')
# @jwt_required(optional=True)
def summary_home():
    return render_template('services/summary.html')


@summary_bp.route('/summary-text', methods=["POST"])
def summary_text():
    data = request.get_json()
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"error": "No comment provided"}), 400

    return T5Summary().summarize(user_text=user_text)
