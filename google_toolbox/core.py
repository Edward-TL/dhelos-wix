
import os
import json
from dataclasses import dataclass, field
from typing import Optional, Literal
from collections import OrderedDict

from enum import Enum

from dotenv import dotenv_values

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials as OAuthCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import gspread

from google_toolbox.gdrive import GoogleDrive


class AuthMethodClass(Enum):
    """Authentication method for Google services."""
    OAUTH = "oauth"
    SERVICE_ACCOUNT = "service_account"

AuthMethod = Literal[
    "service_account",
    "oauth"
]


def get_env_vars(filepath: str = None) -> dict:
    """
    Reads an .env file if a path is provided,
    otherwise returns the environment variables from the OS.
    """
    if filepath and os.path.exists(filepath):
        return dotenv_values(filepath)
    
    # Return environment variables from the OS sorted alphabetically
    env_dict = OrderedDict()
    for key in sorted(os.environ.keys()):
        env_dict[key] = os.environ[key]
    return env_dict


@dataclass
class DriveScopes:
    DRIVE: str = 'https://www.googleapis.com/auth/drive'
    SHEETS: str = 'https://www.googleapis.com/auth/spreadsheets'


@dataclass
class GoogleEnv:
    """Google environment variables and credentials manager.
    
    Supports two authentication methods:
    - AuthMethod.SERVICE_ACCOUNT: Uses service account JSON credentials
    - AuthMethod.OAUTH: Uses OAuth 2.0 credentials (token-based)
    """
    
    auth_method: AuthMethod | AuthMethodClass = "service_account"
    env_path: Optional[str] = None
    json_credentials: Optional[str] = None
    env_var_name: str = 'GOOGLE_CREDENTIALS'
    oauth_token: Optional[dict | str] = None
    scopes: tuple = field(default_factory=lambda: (
        DriveScopes.DRIVE,
        DriveScopes.SHEETS,
    ))
    
    # These will be set in __post_init__
    credentials: service_account.Credentials = field(init=False, default=None)
    creds_with_scope: service_account.Credentials = field(init=False, default=None)

    def __post_init__(self):
        # Ensure oauth_token is a dict if passed as string
        if self.oauth_token and isinstance(self.oauth_token, str):
            try:
                self.oauth_token = json.loads(self.oauth_token)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse oauth_token string as JSON: {e}")

        self.creds_info = self._get_creds_info()

        if self.auth_method in {AuthMethodClass.SERVICE_ACCOUNT, "service_account"}:
            self._load_service_account_credentials()
        elif self.auth_method in {AuthMethodClass.OAUTH, "oauth"}:
            self._load_oauth_credentials()
        else:
            raise ValueError(f"Unsupported auth method: {self.auth_method}")
    
    def _get_creds_info(self) -> dict:
        """Load credentials info from file or environment variable."""
        if self.auth_method in {AuthMethodClass.OAUTH, "oauth"} and self.oauth_token:
            return {}  # Not needed for OAuth if token provided directly

        if self.env_path:
            # Load from .env file - expects JSON string in file
            env_vals = get_env_vars(self.env_path)
            creds_info = env_vals.get(self.env_var_name)
            if creds_info:
                return json.loads(creds_info)
            else:
                raise ValueError(f"'{self.env_var_name}' not found in {self.env_path}")
            
        elif self.json_credentials:
            return json.load(open(self.json_credentials))
        else:
            # Load from OS environment variable
            creds_json = os.getenv(self.env_var_name)
            if not creds_json:
                # If using OAuth and we have a token, we might not need CREDENTIALS env var for client config
                # unless we need to refresh with client secret.
                # But for simplicity, if oauth_token is NOT provided, we need something.
                if self.auth_method in {AuthMethodClass.OAUTH, "oauth"} and self.oauth_token:
                    return {}
                return {} # Return empty if not found, let specific loaders complain if they need it code
            return json.loads(creds_json)
    
    def _load_service_account_credentials(self):
        """Load credentials using Service Account authentication.
        """
        if not self.creds_info:
             raise ValueError(f"Environment variable '{self.env_var_name}' not set or empty for Service Account")

        self.credentials = service_account.Credentials.from_service_account_info(self.creds_info)
        self.creds_with_scope = self.credentials.with_scopes(self.scopes)
    
    def _load_oauth_credentials(self):
        """Load credentials using OAuth 2.0 authentication.
        
        Uses InstalledAppFlow for client credentials JSON files if no token is available.
        Checks for token expiration and refreshes if a refresh_token is present.
        """
        creds = None
        token_path = None

        # 1. Try to load token from oauth_token (direct dict/string)
        if self.oauth_token:
            creds = OAuthCredentials.from_authorized_user_info(self.oauth_token, list(self.scopes))
        
        # 2. If no token yet, try to load cached token from file
        else:
            # Determine token cache path
            if self.json_credentials:
                token_path = self.json_credentials.replace('.json', '_token.json')
            else:
                token_path = 'token.json'
            
            if os.path.exists(token_path):
                try:
                    creds = OAuthCredentials.from_authorized_user_file(token_path, list(self.scopes))
                except ValueError as e:
                    # Token file is corrupted or missing required fields
                    print(f"Invalid cached token: {e}")
                    creds = None

        # 3. Check validity and refresh if needed
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired OAuth token...")
                creds.refresh(Request())
                
                # If we loaded from a file, update it
                if token_path and os.path.exists(token_path):
                     with open(token_path, 'w') as token_file:
                        token_file.write(creds.to_json())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None

        # 4. If still no valid credentials, run the OAuth flow (if possible)
        if not creds or not creds.valid:
            if not self.json_credentials:
                # In serverless, we usually can't run the flow
                if self.oauth_token:
                    raise ValueError("OAuth token is expired and refresh failed. Please generate a new token.")
                raise ValueError(
                    "OAuth requires a client credentials JSON file for the initial flow. "
                    "Provide 'json_credentials' parameter with path to your OAuth client file."
                )
            
            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                self.json_credentials, 
                scopes=list(self.scopes)
            )
            # access_type='offline' ensures we get a refresh_token
            creds = flow.run_local_server(port=8080, access_type='offline', prompt='consent')
            
            # Save token for next run if we have a path
            path_to_save = token_path or (self.json_credentials.replace('.json', '_token.json') if self.json_credentials else 'token.json')
            with open(path_to_save, 'w') as token_file:
                token_file.write(creds.to_json())
        
        self.credentials = creds
        self.creds_with_scope = creds
    
    def sheets_client(self) -> gspread.Client:
        """Get authorized gspread client for Google Sheets."""
        return gspread.authorize(self.creds_with_scope)

    def drive_service(self, main_folder_id: Optional[str] = None) -> GoogleDrive:
        """Get GoogleDrive service instance."""
        return GoogleDrive(
            credentials = self.creds_with_scope,
            main_folder_id = main_folder_id
        )


# Create default instance (will fail if GOOGLE env var not set - catch at import time if needed)
# Google = GoogleEnv()