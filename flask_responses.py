
from flask import Response as FlaskResponse
from dotenv import load_dotenv
import json
import os
import requests

try:
    load_dotenv()
except Exception as e:
    return error_response(
        f"Failed to load environment variables: {str(e)}",
        wix_source_flag="UNKNOWN"
    )


def send_discord_message(message: str, level: str, wix_source_flag: str) -> None:
    """
    Sends a formatted message to Discord via webhook.
    
    Args:
        message (str): The message content
        level (str): The log level (ERROR, SUCCESS, SKIPPED)
        wix_source_flag (str): The source identifier of the request
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("WARNING: DISCORD_WEBHOOK_URL not configured. Skipping Discord notification.")
        return

    formatted_message = f"{level} | {wix_source_flag} --> {message}"
    
    try:
        payload = {"content": formatted_message}
        requests.post(webhook_url, json=payload)
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
