# controllers/main_controller.py
from flask import Blueprint, render_template, request, jsonify
from app.services.summarize.t5 import T5Summary
# from app.services.summarize.job_service import JobService

summary_bp = Blueprint('summary', __name__, url_prefix='/summary')


@summary_bp.route('/')
def summary_home():
    return render_template('services/summary.html')


@summary_bp.route('/summary-text', methods=["POST"])
def summary_text():
    data = request.get_json()
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"error": "No comment provided"}), 400

    return T5Summary().summarize(texts=user_text)


# @summary_bp.route('/upload-csv', methods=["POST"])
# def upload_csv():
#     try:
#         if "file" not in request.files:
#             return jsonify({"error": "No file uploaded"}), 400

#         file = request.files["file"]

#         job_info = JobService.upload_csv_and_queue(file)

#         return jsonify({
#             "message": "File uploaded successfully, job queued",
#             **job_info
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
