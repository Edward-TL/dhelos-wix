
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Define scopes (must match what you use in GoogleEnv)
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

def generate_token(client_secrets_file: str, token_abs_path: str = 'token.json') -> None:
    """
    Generate an OAuth token using the provided client secrets file.
    
    Args:
        client_secrets_file (str): Path to the client secrets JSON file.
    """
    print("--- OAuth Token Generator ---")
    
    if not os.path.exists(client_secrets_file):
        print(f"Error: File '{client_secrets_file}' not found.")
        return

    print(f"Using client secrets from: {client_secrets_file}")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
        # access_type='offline' is required to get a refresh_token
        # prompt='consent' forces a new refresh_token even if one was previously issued
        creds = flow.run_local_server(port=8080, access_type='offline', prompt='consent')
        
        # Save the credentials to token.json
        token_content = creds.to_json()
        with open(token_abs_path, 'w') as token_file:
            token_file.write(token_content)
            
        print("\nSuccess! 'token.json' has been created.")
        print("This file contains the 'refresh_token' and other fields needed for Cloud Run.")
        print("\nReview the content:")
        print(token_content)
        print("\nCopy the content ABOVE and set it as your GOOGLE_OAUTH_TOKEN environment variable.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    generate_token()
