from flask import jsonify, redirect, render_template, url_for, Blueprint, request
from app.models.draft.draft_res import ProcessedResults
from app.models.draft.draft import Draft
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/u')

@dashboard_bp.route('/draft/<string:draft_id>/dashboard', methods=['GET', 'POST'])
@jwt_required(optional=True)
def dashboard(draft_id):
    current_user = get_jwt_identity()
    if not current_user:
        # For API calls (POST), return a JSON error. For web pages (GET), redirect.
        if request.method == 'POST':
            return jsonify({"error": "Authentication required"}), 401
        return redirect(url_for('login.login_page')) 
    
    # Handle POST request to fetch dashboard data asynchronously
    draft_title = Draft.query.filter_by(id=draft_id).first().title
    if request.method == 'POST':
        dashboard_data = ProcessedResults.query.filter_by(draft_id=draft_id).first()

        if dashboard_data:
            # FIX: Wrap the results in a JSON object with a "results" key
            # to match what the frontend Javascript expects.
            return jsonify({"results": dashboard_data.results})
        else:
            # Inform the client that the data is not ready yet
            return jsonify({"status": "processing"}), 202

    # Handle GET request to render the initial page shell
    # The frontend will then make a POST request to this same URL to get the data.
    return render_template('dashboard/dashboard.html', draft_id=draft_id, title=draft_title)

