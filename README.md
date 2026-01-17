# Cloud Run Service for structuring API POST JSON data to Google Drive excel and parquet files

Cloud Run service that receives API POST JSON data and stores data in Google Drive excel and parquet files.

## Features

- Receives API POST JSON data
- Flattens nested JSON data into single-level format
- Appends data to Excel and parquet files stored in Google Drive
- Auto-creates headers if Excel file is empty

## Project Structure

```
├── main.py                            # Cloud Run entry point (uses google_toolbox)
├── google_toolbox/                    # Consolidated Google API module
│   ├── core.py                        # GoogleEnv and Auth classes
│   └── gdrive.py                      # GoogleDrive wrapper
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Container configuration
└── tests/                             # Unit tests and samples
    ├── sample_payload.json            # Sample Wix webhook payload
    └── test_dictionary_cleaning.py    # Unit tests
```

## Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest  # for testing
   ```

2. **Set up authentication** (choose one method):

   ### Option A: Service Account (Recommended for Cloud Run)
   
   Best for server-to-server interaction and production deployments.
   
   #### **Settings Procedure:**
   1. **Enable APIs**: Go to [Google Cloud Console](https://console.cloud.google.com/) → **APIs & Services** → **Library**. Enable:
      - `Google Drive API`
      - `Google Sheets API`
   2. **Create Service Account**: Go to **IAM & Admin** → **Service Accounts**.
      - Click **+ CREATE SERVICE ACCOUNT**.
      - Give it a name (e.g., `dhelos-clean-plan-sells`).
      - Click **CREATE AND CONTINUE**.
      - (Optional) Grant "Editor" role if needed, or skip to manage permissions per-file.
      - Click **DONE**.
   3. **Generate JSON Key**: Click on the new service account → **Keys** tab.
      - Click **ADD KEY** → **Create new key**.
      - Select **JSON** and click **CREATE**.
      - Save the file as `service_account.json`. **Never commit this file to git.**
   4. **Share Drive Access**: Open the Google Drive folder or Excel file you want to access.
      - Click **Share**.
      - Paste the service account's email address (found in the IAM dashboard).
      - Grant at least **Editor** permissions.
   
   **Usage:**
   ```python
   from google_toolbox import GoogleEnv
   
   # Load from local JSON file
   google_env = GoogleEnv(json_credentials="service_account.json")
   
   # OR: Load from environment variable (Best for Cloud Run)
   # Set GOOGLE_CREDENTIALS env var with the JSON content string
   google_env = GoogleEnv()
   ```

   ### Option B: OAuth 2.0 (For local development & Cloud Run with User Account)
   
   Best for accessing files owned by your personal Google account.
   
   #### **Settings Procedure:**
   1. **Create Credentials**: 
      - Go to **APIs & Services** → **Credentials**.
      - Create **OAuth client ID** (Desktop app).
      - Download JSON, save as `secrets/client_secrets.json`.

   2. **Generate Token (Required for Cloud Run)**:
      Since Cloud Run cannot open a browser, you must generate a token locally first.
      
      ```bash
      # Run the helper script
      python generate_token.py
      ```
      - Follow the prompt to authorize access.
      - A `token.json` file will be created.

   3. **Configure Environment**:
      
      **Local Development:**
      - Set `GOOGLE_OAUTH_TOKEN` to the content of `token.json`.
      - OR just leave `token.json` in the working directory (automatic fallback).

      **Cloud Run:**
      - Copy the content of `token.json`.
      - Create an environment variable `GOOGLE_OAUTH_TOKEN` with this value.
   
   **Usage:**
   Option a:
   ```python
   from google_toolbox import GoogleEnv, AuthMethodClass
   
   # Automatically checks GOOGLE_OAUTH_TOKEN env var first
   google_env = GoogleEnv(
      auth_method=AuthMethodClass.OAUTH, 
      json_credentials="secrets/token.json" # Fallback/Initial setup
   )
   ```

   Option b:
   ```python
   from google_toolbox import GoogleEnv, AuthMethodClass
   
   # Automatically checks GOOGLE_OAUTH_TOKEN env var first
   google_env = GoogleEnv(
      auth_method=AuthMethodClass.OAUTH, 
      oauth_token="{'token': 'your-token-here', 'refresh_token': 'your-refresh-token-here', 'token_uri': 'https://oauth2.googleapis.com/token', 'client_id': 'your-client-id', 'client_secret': 'your-client-secret'}"
   )
   ```

3. **Set environment variables:**
   ```bash
   export GOOGLE_DRIVE_FILE_ID=your-file-id
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
   ```

4. **Run locally:**
   ```bash
   functions-framework --target load_to_excel --debug
   ```

5. **Test with sample payload:**
   ```bash
   curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d @tests/sample_payload.json
   ```

## Deployment

### Prerequisites

1. Enable GCP APIs:
   ```bash
   gcloud services enable run.googleapis.com artifactregistry.googleapis.com drive.googleapis.com
   ```

2. Create Artifact Registry repository:
   ```bash
   gcloud artifacts repositories create dhelos-functions \
     --repository-format=docker \
     --location=us-central1
   ```

### GitHub Secrets Required

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | Google Cloud project ID |
| `GCP_SA_KEY` | Service account JSON key (base64 encoded) |
| `GOOGLE_DRIVE_FILE_ID` | Target Excel file ID in Google Drive |

### Manual Deploy

```bash
# Build and push
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/cloud-run-service .
docker push us-central1-docker.pkg.dev/PROJECT_ID/cloud-run-service

# Deploy
gcloud run deploy cloud-run-service \
  --image us-central1-docker.pkg.dev/PROJECT_ID/cloud-run-service \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_DRIVE_FILE_ID=your-file-id"
```

## Testing

```bash
python -m pytest tests/test_dictionary_cleaning.py -v
```

## License

MIT License - see [LICENSE](LICENSE)
