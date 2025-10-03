from flask import jsonify

def success_response(data=None, message="Success", status_code=200, cookie=None):
    return jsonify({
        "status": True,
        "message": message,
        "data": data
    }), status_code

def error_response(message="An error occurred", status_code=400, data=None):
    res = jsonify({
        "status": False,
        "message": message,
        "data": data
    })

    return res, status_code
