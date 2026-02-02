
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
from google.cloud import secretmanager

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


def refresh_and_update_token(
    creds: OAuthCredentials,
    project_id: Optional[str] = None,
    secret_name: Optional[str] = None
) -> OAuthCredentials:
    """
    Refresh an expired OAuth token and optionally update it in Google Secret Manager.
    
    Args:
        creds: The OAuth credentials to refresh
        project_id: GCP project ID for Secret Manager (optional)
        secret_name: Name of the secret to update (optional)
    
    Returns:
        Refreshed OAuth credentials
    
    Raises:
        Exception: If token refresh fails
    """
    print("[OAuth] Refreshing expired token...")
    
    try:
        # Refresh the token
        creds.refresh(Request())
        print("[OAuth] Token refreshed successfully")
        
        # Update Secret Manager if configured
        if project_id and secret_name:
            try:
                print(f"[Secret Manager] Updating secret '{secret_name}'...")
                
                # Create Secret Manager client
                client = secretmanager.SecretManagerServiceClient()
                
                # Prepare the secret payload
                token_json = creds.to_json()
                payload = token_json.encode('UTF-8')
                
                # Build the parent secret name
                parent = client.secret_path(project_id, secret_name)
                
                # Add new secret version
                response = client.add_secret_version(
                    request={
                        "parent": parent,
                        "payload": {"data": payload}
                    }
                )
                
                print(f"[Secret Manager] Secret updated successfully: {response.name}")
                
            except Exception as secret_error:
                # Log but don't fail - token is still refreshed
                print(f"[Secret Manager] Warning: Failed to update secret: {secret_error}")
                print("[Secret Manager] Token was refreshed but not persisted to Secret Manager")
        else:
            print("[Secret Manager] No project_id/secret_name provided, skipping secret update")
        
        return creds
        
    except Exception as e:
        print(f"[OAuth] Failed to refresh token: {e}")
        raise


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
    # Secret Manager configuration for OAuth token refresh
    secret_project_id: Optional[str] = None
    secret_name: Optional[str] = None
    
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
                # Use the new refresh function with Secret Manager support
                creds = refresh_and_update_token(
                    creds,
                    project_id=self.secret_project_id,
                    secret_name=self.secret_name
                )
                
                # If we loaded from a file, update it (local development)
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