from flask import jsonify


def success(message, data=None):
    """
    Standard success response
    """
    return jsonify({
        "status": "success",
        "message": message,
        "data": data if data is not None else {}
    }), 200


def error(message, status_code=400):
    """
    Standard error response
    """
    return jsonify({
        "status": "error",
        "message": message
    }), status_code