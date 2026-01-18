import warnings
# Suppress any UserWarning related to pkg_resources to avoid the deprecation notice
warnings.filterwarnings("ignore", ".*pkg_resources.*")

"""
MAIN FILE

PURPOSE: Cloud Run function to receive Wix Plan Sales webhooks
         and store data in Google Drive (Parquet + Excel)

Author: Edward Toledo Lopez <edward_tl@hotmail.com>
"""

import os
import json
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv

import pandas as pd
from functions_framework import http as functions_http
from flask import (
    Response as FlaskResponse,
    Request as FlaskRequest
)

from google_toolbox import GoogleEnv

from helpers import (
    is_valid_request,
    flat_dictionary,
    is_new_data
)

from flask_responses import (
    error_response,
    bad_resquest_response,
    success_response,
    skipped_response
)

load_dotenv()

@functions_http
def load_to_drive(request: FlaskRequest) -> FlaskResponse:
    """
    HTTP entry point for receiving Wix Plan Sales data.
    
    Receives a POST request with JSON body from Wix API,
    flattens the data, and stores in Parquet + Excel files on Google Drive.
    
    Returns:
        FlaskResponse with status and message
    """
    # Only accept POST requests
    bad_response, data = is_valid_request(request)
    if bad_response is not None:
        return bad_response

    # Flatten the nested dictionary
    flat_data = flat_dictionary(data.get('data', {}))
    info = {
        'flat_data': flat_data,
        'raw_data': data
    }

    wix_triger = flat_data.get('_context_trigger_key')
    if wix_triger is None:
        return bad_resquest_response(
            f"Failed to extract `_context_trigger_key` from response: {str(e)}",
            wix_source_flag="UNKNOWN"
        )

    # Load configuration
    try:
        OAUTH_TOKEN = json.loads(
            os.getenv("OAUTH_TOKEN")
        )
        FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

        config = json.loads(
            os.getenv("CONFIG")
        )[wix_triger]
        
        file_name = config["FILE_NAME"]
        parquet_file_id = config["PARQUET_FILE_ID"]
        excel_file_id = config["EXCEL_FILE_ID"]
        filter_field = config["FILTER_FIELD"]


    except Exception as e:
        return error_response(
            f"Failed to load config: {str(e)}",
            wix_source_flag=wix_triger
        )
    
    # Validate folder ID
    if not FOLDER_ID:
        return error_response(
            "GOOGLE_DRIVE_FOLDER_ID not configured in environment variables",
            wix_source_flag=wix_triger
        )
    
    # Initialize Google Drive
    try:
        google_env = GoogleEnv(
            auth_method = "oauth",
            oauth_token = OAUTH_TOKEN
        )
        drive = google_env.drive_service(main_folder_id=FOLDER_ID)
    except Exception as e:
        return error_response(
            f"Failed to initialize Google Drive: {str(e)}",
            wix_source_flag=wix_triger
        )
    
    # Confirm the existence of the parquet_id:
    if parquet_file_id == "":
        print("Parquet file ID not configured in environment variables. Getting file ID from Google Drive...")
        parquet_file_id = drive.get_file_id(f"{file_name}.parquet")
        excel_file_id = drive.get_file_id(f"{file_name}.xlsx")
            
    # Upload JSON record to Drive
    try:
        json_buffer = BytesIO()
        # Ensure we write bytes, json.dumps returns str so encode it
        for reference, json_data in info.items():
            json_buffer.write(json.dumps(json_data, indent=2).encode('utf-8'))

            drive.upload_buffer(
                json_buffer,
                f"{file_name}_{reference}.json",
                mimetype='application/json'
            )
            print(f"JSON record uploaded: {file_name}.json")
    except Exception as e:
        print(f"Failed to upload JSON record: {e}")
            # Continue execution as this is just a record

    # Step 1: Check if file exists
    update_df = False
    if parquet_file_id:
        # Step 2.a: File exists - download and check for new data
        print("Downloading parquet file...")
        try:
            buffer = drive.download_file(parquet_file_id)

            if buffer:
                df = pd.read_parquet(buffer)
                print("Parquet file downloaded successfully")
                update_df = is_new_data(
                    df,
                    flat_data,
                    compare_col = filter_field
                )
                print("Data is new:", update_df)
            else:
                # Download failed, treat as new file
                print("Parquet file downloaded FAILED. Creating new file...")
                df = pd.DataFrame()
                update_df = True
        except Exception as e:
            return error_response(
                f"Failed to download parquet: {str(e)}",
                wix_source_flag=wix_triger
            )
    else:
        # Step 2.b: File does not exist
        print("Parquet file DOES NOT EXIST. Creating new file...")
        df = pd.DataFrame()
        update_df = True
    
    flat_data['request_date'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    df_new = pd.DataFrame([flat_data])
    
    # Step 3.a: If update is not needed
    if not update_df:
        return skipped_response(
            "Data already exists in file",
            wix_source_flag=wix_triger
        )
    
    # Step 3.b: Update DataFrame if needed
    # Append new data
    df = pd.concat([df, df_new], ignore_index=True)
    print("Dataframe updated successfully. New shape:", df.shape)

    # Step 4: Save and upload files from buffers
    formats_ids = {
        'parquet': parquet_file_id,
        'excel': excel_file_id
    }
    
    response = {
        file_format: drive.upload_df_to_drive(
            df = df,
            file_name = file_name,
            folder_id = FOLDER_ID,
            file_format = file_format,
            file_id = file_id
        ) for file_format, file_id in formats_ids.items()
    }
            
    response['rows'] = len(df)

    return success_response(
        "Data added",
        wix_source_flag=wix_triger,
        data=response
    )