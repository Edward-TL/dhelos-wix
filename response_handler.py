
from flask import Response as FlaskResponse
import json
import os
import requests

from loader import ENV_VALS

def send_discord_message(message: str, level: str, wix_source_flag: str) -> None:
    """
    Sends a formatted message to Discord via webhook.
    
    Args:
        message (str): The message content
        level (str): The log level (ERROR, SUCCESS, SKIPPED)
        wix_source_flag (str): The source identifier of the request
    """
    if not ENV_VALS.DISCORD_WEBHOOK_URL:
        print("WARNING: DISCORD_WEBHOOK_URL not configured. Skipping Discord notification.")
        return

    formatted_message = f"[{level}] {wix_source_flag} --> {message}"
    
    try:
        payload = {"content": formatted_message}
        requests.post(ENV_VALS.DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Failed to send Discord notification: {str(e)}")

def error_response(message: str, wix_source_flag: str, status: int = 500) -> FlaskResponse:
    """
    Returns a Flask Response with an error message and status code.
    Prints the message and sends to Discord before returning.
    """
    print(f"ERROR: {message}")
    send_discord_message(message, "ERROR", wix_source_flag)
    return FlaskResponse(
        json.dumps({"error": message}),
        status=status,
        mimetype='application/json'
    )

def bad_resquest_response(message: str, wix_source_flag: str, status: int = 404) -> FlaskResponse:
    """
    Returns a Flask Response with an error message and status code.
    Prints the message and sends to Discord before returning.
    """
    print(f"ERROR: {message}")
    send_discord_message(message, "ERROR", wix_source_flag)
    return FlaskResponse(
        json.dumps({"error": message}),
        status=status,
        mimetype='application/json'
    )

def success_response(message: str, wix_source_flag: str, data: dict = None, status: int = 200) -> FlaskResponse:
    """
    Returns a Flask Response with a success status, message, and optional data.
    Prints the message and sends to Discord before returning.
    """
    print(f"SUCCESS: {message}")
    send_discord_message(message, "SUCCESS", wix_source_flag)
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

def skipped_response(message: str, wix_source_flag: str, status: int = 200) -> FlaskResponse:
    """
    Returns a Flask Response with a skipped status and message.
    Prints the message and sends to Discord before returning.
    """
    print(f"SKIPPED: {message}")
    send_discord_message(message, "SKIPPED", wix_source_flag)
    return FlaskResponse(
        json.dumps({
            "status": "skipped",
            "message": message
        }),
        status=status,
        mimetype='application/json'
    )

# Response handler mapping based on status codes
RESPONSE_HANDLER_MAP = {
    200: skipped_response,      # OK - Object found/Action completed
    201: success_response,      # CREATED - Success on creating
    400: bad_resquest_response, # BAD REQUEST - Request does not have all values needed
    404: bad_resquest_response, # NOT FOUND - Request is OK. Object was not found
    406: error_response,        # NOT ACCEPTABLE - ValueError type on request values
    409: error_response,        # CONFLICT - Request is OK. Object has a conflict
    500: error_response         # INTERNAL SERVER ERROR - General error fallback
}

def handle_response(message: str, wix_source_flag: str, status: int, data: dict = None) -> FlaskResponse:
    """
    Unified response handler that routes to the correct response function based on status code.
    
    Args:
        message (str): The message content
        wix_source_flag (str): The source identifier of the request
        status (int): HTTP status code (200, 201, 400, 404, 406, 409, 500)
        data (dict, optional): Additional data to include in success responses
    
    Returns:
        FlaskResponse: Flask response object with appropriate status and message
    
    Raises:
        ValueError: If status code is not supported
    """
    if status not in RESPONSE_HANDLER_MAP:
        # Default to error_response for unknown status codes
        print(f"WARNING: Unknown status code {status}, defaulting to error_response")
        return error_response(f"Unknown status code: {status}. {message}", wix_source_flag, status)
    
    handler_func = RESPONSE_HANDLER_MAP[status]
    
    # success_response is the only function that accepts a 'data' parameter
    if handler_func == success_response and data is not None:
        return success_response(message, wix_source_flag, data, status)
    elif handler_func == success_response:
        return success_response(message, wix_source_flag, None, status)
    else:
        return handler_func(message, wix_source_flag, status)

