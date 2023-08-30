import boto3
import json
from datetime import datetime, timedelta


def lambda_handler(event, context):
    """Function will gather yesterdays cloud trial events and makes into into a single json file and saves it to s3 bucket"""
    # Initialize the Boto3 client for CloudTrail and S3
    cloudtrail_client = boto3.client('cloudtrail')
    s3_client = boto3.client('s3')

    # Define the time range for yesterday 12 AM to today 12 AM
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = end_time.replace(hour=0, minute=0, second=0, microsecond=0)

    # Format the time in the required string format (UTC)
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Create a list to store all CloudTrail events
    all_events = []

    # Paginate through CloudTrail events
    paginator = cloudtrail_client.get_paginator('lookup_events')
    for page in paginator.paginate(
            StartTime=start_time_str,
            EndTime=end_time_str
    ):
        # Add the events on the current page to the list
        all_events.extend(page['Events'])

    # Define the output JSON file path
    output_file_path = '/tmp/cloudtrail_events.json'

    # Save all events to a JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(all_events, output_file, indent=4,
                  sort_keys=True, default=str)

    print(f"CloudTrail events saved to {output_file_path}")

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_formatted = yesterday.strftime('%d-%m-%Y')

    # Specify the S3 bucket and object key where you want to upload the JSON file
    s3_bucket = 'aravindetagi'
    s3_object_key = f'from_lambda/cloudtrail_events-{yesterday_formatted}.json'

    # Upload the JSON file to S3
    s3_client.upload_file(output_file_path, s3_bucket, s3_object_key)

    print(
        f"Uploaded JSON file to S3 bucket: s3://{s3_bucket}/from_lambda/{s3_object_key}")

    # Clean up the temporary local JSON file
    import os
    os.remove(output_file_path)
