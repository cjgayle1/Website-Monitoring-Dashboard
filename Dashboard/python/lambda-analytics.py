import json
import boto3
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('GA_Stats')

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'loyal-saga-400818-51d91bb184ce.json' 
PROPERTY_ID = '435728775'

def lambda_handler(event, context):
    credentials = service_account.Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES)
    client = BetaAnalyticsDataClient(credentials=credentials)

    # Fetching multiple metrics and dimensions
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[
            {"name": "country"}, {"name": "browser"}, {"name": "date"}
        ],
        metrics=[
            {"name": "activeUsers"}, {"name": "screenPageViews"}, 
            {"name": "newUsers"}, {"name": "averageSessionDuration"}
        ],
        date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]  # As an example, pulling data from 2020 to today
    )

    response = client.run_report(request)
    
    # Process each row in the response
    items = []
    for row in response.rows:
        item = {
            'Date': row.dimension_values[2].value,  # Assuming date is the third dimension
            'Country': row.dimension_values[0].value,
            'Browser': row.dimension_values[1].value,
            'ActiveUsers': int(row.metric_values[0].value),
            'PageViews': int(row.metric_values[1].value),
            'NewUsers': int(row.metric_values[2].value),
            'AvgSessionDuration': float(row.metric_values[3].value)
        }
        items.append(item)
    
    # Write data to DynamoDB
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Data successfully written to DynamoDB"}, indent=4)
    }



# for testing purposes

# def run_report():
#     """Google Analytics Data API V1 Beta Example."""
#     credentials = service_account.Credentials.from_service_account_file(
#         KEY_FILE_LOCATION, scopes=SCOPES)

#     client = BetaAnalyticsDataClient(credentials=credentials)
#     request = RunReportRequest(
#         property=f"properties/{PROPERTY_ID}",
#         dimensions=[{"name": "city"}],
#         metrics=[{"name": "activeUsers"}],
#         date_ranges=[{"start_date": "2021-03-31", "end_date": "today"}]
#     )

#     response = client.run_report(request)

#     # Process and print the response in a readable JSON format
#     readable_json = {
#         'cities': [
#             {'name': row.dimension_values[0].value, 'activeUsers': row.metric_values[0].value}
#             for row in response.rows
#         ],
#         'currency': response.metadata.currency_code,
#         'timezone': response.metadata.time_zone
#     }
    
#     print(json.dumps(readable_json, indent=4))

# if __name__ == "__main__":
#     run_report()
