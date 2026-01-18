
from flask import Response as FlaskResponse
import json

def error_response(message: str, status: int = 500) -> FlaskResponse:
    """
    Returns a Flask Response with an error message and status code.
    Prints the message before returning.
    """
    print(f"ERROR: {message}")
    return FlaskResponse(
        json.dumps({"error": message}),
        status=status,
        mimetype='application/json'
    )

def bad_resquest_response(message: str, status: int = 404) -> FlaskResponse:
    """
    Returns a Flask Response with an error message and status code.
    Prints the message before returning.
    """
    print(f"ERROR: {message}")
    return FlaskResponse(
        json.dumps({"error": message}),
        status=status,
        mimetype='application/json'
    )

def success_response(message: str, data: dict = None, status: int = 200) -> FlaskResponse:
    """
    Returns a Flask Response with a success status, message, and optional data.
    Prints the message before returning.
    """
    print(f"SUCCESS: {message}")
    response_body = {
        "status": "success",
        "message": message
    }
    if data:
        response_body.update(data)
        
    return FlaskResponse(
        json.dumps(response_body),
        status=status,
        mimetype='application/json'
    )

def skipped_response(message: str, status: int = 200) -> FlaskResponse:
    """
    Returns a Flask Response with a skipped status and message.
    Prints the message before returning.
    """
    print(f"SKIPPED: {message}")
    return FlaskResponse(
        json.dumps({
            "status": "skipped",
            "message": message
        }),
        status=status,
        mimetype='application/json'
    )
