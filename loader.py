"""
Loader module for the Wix Plan Sales webhook handler.
"""

import os
import json
from dotenv import load_dotenv
from dataclasses import dataclass, field

load_dotenv()

@dataclass
class EnvVals:
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL")
    FOLDER_ID: str = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
    CONFIG: dict = field(default_factory=lambda: json.loads(os.getenv("CONFIG")))
    OAUTH_TOKEN: dict = field(default_factory=lambda: json.loads(os.getenv("OAUTH_TOKEN")))
    # Secret Manager configuration for OAuth token refresh
    SECRET_PROJECT_ID: str = os.getenv("GOOGLE_SECRET_PROJECT_ID")
    SECRET_NAME: str = os.getenv("GOOGLE_SECRET_NAME")

ENV_VALS = EnvVals()