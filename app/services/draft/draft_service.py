# app/services/auth/login.py

from app.models.draft.draft import Draft
from app.extensions import db
from flask import jsonify, make_response, json
from app.utils.response import success_response, error_response
from app.models.draft.draft import Draft
from app.config.aws_config import QUEUE_URL
from app.services.aws_clients import sqs_client


class DraftService:
    
    '''
    - title: draft title
    - desc: a short description of the draft
    - file_url: csv file url
    '''
    @staticmethod
    def add_draft(title, desc, file_url, user_id):

        if len(desc) > 700:
            return error_response("Description can't be greater than 700.", 401)
        
        draft = Draft(
            title=title,
            desc=desc,
            draft_file=file_url,
            user_id=user_id
        )

        try:

            db.session.add(draft)
            db.session.commit()

            print(draft.id, "helloll")
            message_body = json.dumps({"file_key": draft.id})
            sqs_client.send_message(QueueUrl=QUEUE_URL, MessageBody=message_body)
        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}") 
            return error_response(f"Failed to add draft due to a internal error.", 500)
        


        return success_response(
            message="Draft added succesfully!",
            data=draft.to_dict(),
            status_code=201
        )

    @staticmethod
    def draft_list(user_id):
        try:
            drafts = Draft.query.filter_by(user_id=user_id).order_by(Draft.created_at.desc()).all()
        except Exception as e:
            print(f"Database Error: {e}") 
            return error_response(f"Failed to get list of drafts due to a internal error.", 500)

        return success_response(
            message='loadind drafts...',
            data=[d.to_dict() for d in drafts]
        )
