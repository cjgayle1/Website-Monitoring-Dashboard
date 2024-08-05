import json
import boto3
import os
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, BatchRunReportsRequest
from decimal import Decimal
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('GA_Stats3')

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def lambda_handler(event, context):
    # Load credentials from an environment variable
    creds_json = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
    credentials = service_account.Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = BetaAnalyticsDataClient(credentials=credentials)
    PROPERTY_ID = os.environ['PROPERTY_ID']
    
    requests = [
        RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[{"name": "Date"}],
            metrics=[{"name": "activeUsers"}, {"name": "newUsers"},
                     {"name": "screenPageViews"}, {"name": "averageSessionDuration"}, {"name": "eventCount"}, 
                     {"name": "sessions"}],
            date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
        ),
        RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            metrics=[ {"name": "activeUsers"},
                     {"name": "screenPageViews"},  {"name": "eventCount"}, 
                     {"name": "sessions"}],
            date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
        ),
        RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[{"name": "country"}],
            metrics=[{"name": "activeUsers"}],
            date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
        ),
        RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[{"name": "browser"}],
            metrics=[{"name": "activeUsers"}],
            date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
        ),
        RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[{"name": "operatingSystem"}],
            metrics=[{"name": "activeUsers"}],
            date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
        )
    ]

    # Create a BatchRunReportsRequest
    batch_request = BatchRunReportsRequest(
        property=f"properties/{PROPERTY_ID}",
        requests=requests
    )

    # Fetch the batch report
    response = client.batch_run_reports(batch_request)
    print(response)

    # Process the response and structure data for DynamoDB
    report_data = {
        'Date': datetime.utcnow().strftime('%Y-%m-%d')  # Use current date as a unique key for this report
    }

    # Process each report separately
    for i, report in enumerate(response.reports):
        report_key = f'Report{i+1}'
        report_data[report_key] = {}
        if report.rows:
            if requests[i].dimensions:  # Check if dimensions are present
                for row in report.rows:
                    dim_key = ', '.join(dimension.value for dimension in row.dimension_values)
                    metrics = {metric.name: Decimal(str(metric_value.value)) for metric, metric_value in zip(requests[i].metrics, row.metric_values)}
                    report_data[report_key][dim_key] = metrics
            else:
                # Handle metric-only reports
                metrics = {metric.name: Decimal(str(metric_value.value)) for metric, metric_value in zip(requests[i].metrics, report.rows[0].metric_values)}
                report_data[report_key]['Totals'] = metrics

    print(report_data)

    # Generate instanceID based on the current date and time
    now = datetime.utcnow()
    instance_id = (now.year * 10000000000 + now.month * 100000000 + 
                   now.day * 1000000 + now.hour * 10000 + 
                   now.minute * 100 + now.second)
    report_data['instanceID'] = instance_id
    report_data['Data'] = "GA_Stats"

    table.put_item(Item=report_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Data successfully written to DynamoDB"}, indent=4)
    }





# import json
# import boto3
# import os

# from google.oauth2 import service_account
# from google.analytics.data_v1beta import BetaAnalyticsDataClient
# from google.analytics.data_v1beta.types import RunReportRequest, BatchRunReportsRequest
# from decimal import Decimal
# from datetime import datetime

# # Initialize DynamoDB
# dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
# table = dynamodb.Table('GA_Stats')

# SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']


# def lambda_handler(event, context):
#     # Load credentials from an environment variable
#     creds_json = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
#     credentials = service_account.Credentials.from_service_account_info(creds_json, scopes=SCOPES)
#     client = BetaAnalyticsDataClient(credentials=credentials)
#     PROPERTY_ID = os.environ['PROPERTY_ID']
    
    
#     requests = [
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "Date"}],
#             metrics=[{"name": "activeUsers"}, {"name": "newUsers"},
#                      {"name": "screenPageViews"}, {"name": "averageSessionDuration"}, {"name": "eventCount"}, 
#                      {"name": "sessions"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             metrics=[ {"name": "activeUsers"},
#                      {"name": "screenPageViews"},  {"name": "eventCount"}, 
#                      {"name": "sessions"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "country"}],
#             metrics=[{"name": "activeUsers"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "browser"}],
#             metrics=[{"name": "activeUsers"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "operatingSystem"}],
#             metrics=[{"name": "activeUsers"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         )
#     ]

#     # Create a BatchRunReportsRequest
#     batch_request = BatchRunReportsRequest(
#         property=f"properties/{PROPERTY_ID}",
#         requests=requests
#     )

#     # Fetch the batch report
#     response = client.batch_run_reports(batch_request)
#     print(response)

#     # Process the response and structure data for DynamoDB
#     report_data = {
#         'Date': datetime.utcnow().strftime('%Y-%m-%d')  # Use current date as a unique key for this report
#     }

#     # Process each report separately
#     for i, report in enumerate(response.reports):
#         report_key = f'Report{i+1}'
#         report_data[report_key] = {}
#         if report.rows:
#             if requests[i].dimensions:  # Check if dimensions are present
#                 for row in report.rows:
#                     dim_key = ', '.join(dimension.value for dimension in row.dimension_values)
#                     metrics = {metric.name: Decimal(str(metric_value.value)) for metric, metric_value in zip(requests[i].metrics, row.metric_values)}
#                     report_data[report_key][dim_key] = metrics
#             else:
#                 # Handle metric-only reports
#                 metrics = {metric.name: Decimal(str(metric_value.value)) for metric, metric_value in zip(requests[i].metrics, report.rows[0].metric_values)}
#                 report_data[report_key]['Totals'] = metrics

#     print(report_data)
#     # Example of writing the processed data to DynamoDB
#     table.put_item(Item=report_data)
    

#     return {
#         'statusCode': 200,
#         'body': json.dumps({"message": "Data successfully written to DynamoDB"}, indent=4)
#     }



# env variable version

# import json
# import boto3
# import os

# from google.oauth2 import service_account
# from google.analytics.data_v1beta import BetaAnalyticsDataClient
# from google.analytics.data_v1beta.types import RunReportRequest, BatchRunReportsRequest
# from decimal import Decimal
# from datetime import datetime


# RESERVED_KEYS = {
#     "LAMBDA_TASK_ROOT",
#     "AWS_REGION",
#     "AWS_LAMBDA_FUNCTION_MEMORY_SIZE",
#     "AWS_SECRET_ACCESS_KEY",
#     "AWS_DEFAULT_REGION",
#     "AWS_LAMBDA_LOG_GROUP_NAME",
#     "AWS_LAMBDA_LOG_STREAM_NAME",
#     "LAMBDA_RUNTIME_DIR",
#     "AWS_SESSION_TOKEN",
#     "AWS_ACCESS_KEY_ID",
#     "AWS_LAMBDA_FUNCTION_VERSION",
#     "AWS_LAMBDA_RUNTIME_API",
#     "AWS_LAMBDA_FUNCTION_NAME",
# }


# # Initialize DynamoDB
# dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
# table = dynamodb.Table('GA_Stats2')

# SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']


# def lambda_handler(event, context):
#     # Load credentials from an environment variable
#     creds_json = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
#     credentials = service_account.Credentials.from_service_account_info(creds_json, scopes=SCOPES)
#     client = BetaAnalyticsDataClient(credentials=credentials)
#     PROPERTY_ID = os.environ['PROPERTY_ID']
    
    
#     requests = [
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "Date"}],
#             metrics=[{"name": "activeUsers"}, {"name": "newUsers"},
#                      {"name": "screenPageViews"}, {"name": "averageSessionDuration"}, {"name": "eventCount"}, 
#                      {"name": "sessions"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             metrics=[ {"name": "activeUsers"},
#                      {"name": "screenPageViews"},  {"name": "eventCount"}, 
#                      {"name": "sessions"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "country"}],
#             metrics=[{"name": "activeUsers"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "browser"}],
#             metrics=[{"name": "activeUsers"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         ),
#         RunReportRequest(
#             property=f"properties/{PROPERTY_ID}",
#             dimensions=[{"name": "operatingSystem"}],
#             metrics=[{"name": "activeUsers"}],
#             date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]
#         )
#     ]

#     # Create a BatchRunReportsRequest
#     batch_request = BatchRunReportsRequest(
#         property=f"properties/{PROPERTY_ID}",
#         requests=requests
#     )

#     # Fetch the batch report
#     response = client.batch_run_reports(batch_request)
#     print(response)

#     # Process the response and structure data for DynamoDB
#     report_data = {
#         'Date': datetime.utcnow().strftime('%Y-%m-%d')  # Use current date as a unique key for this report
#     }

#     # Process each report separately
#     for i, report in enumerate(response.reports):
#         report_key = f'Report{i+1}'
#         report_data[report_key] = {}
#         if report.rows:
#             if requests[i].dimensions:  # Check if dimensions are present
#                 for row in report.rows:
#                     dim_key = ', '.join(dimension.value for dimension in row.dimension_values)
#                     metrics = {metric.name: Decimal(str(metric_value.value)) for metric, metric_value in zip(requests[i].metrics, row.metric_values)}
#                     report_data[report_key][dim_key] = metrics
#             else:
#                 # Handle metric-only reports
#                 metrics = {metric.name: Decimal(str(metric_value.value)) for metric, metric_value in zip(requests[i].metrics, report.rows[0].metric_values)}
#                 report_data[report_key]['Totals'] = metrics

#     print(report_data)

    
#     instance_counter = int(os.environ['INSTANCE_NUM'])
#     new_instance_id = instance_counter + 1
#     report_data['instanceID'] = new_instance_id
    

#     current_variables = os.environ.copy()
#     current_variables['INSTANCE_NUM'] = str(new_instance_id)
#     print("Current environment variables:", current_variables)

#     # Ensure all keys conform to the required pattern and exclude invalid keys
#     valid_variables = {k: v for k, v in current_variables.items() if k.replace('_', '').isalnum() and k[0].isalpha() and k not in RESERVED_KEYS}
    
#     # Also explicitly print invalid keys for debugging
#     invalid_variables = {k: v for k, v in current_variables.items() if not (k.replace('_', '').isalnum() and k[0].isalpha()) or k in RESERVED_KEYS}
#     print("Invalid environment variables:", invalid_variables)

#     # Update the environment variable using AWS SDK
#     lambda_client = boto3.client('lambda')
#     function_name = context.function_name
    
#     lambda_client.update_function_configuration(
#         FunctionName=function_name,
#         Environment={
#             'Variables': valid_variables
#         }
#     )
    
    
#     table.put_item(Item=report_data)
    

#     return {
#         'statusCode': 200,
#         'body': json.dumps({"message": "Data successfully written to DynamoDB"}, indent=4)
#     }



    # # Fetching multiple metrics and dimensions
    # request1 = RunReportRequest(
    #     property=f"properties/{PROPERTY_ID}",
    #     dimensions=[
    #         {"name": "Date"}
    #     ],
    #     metrics=[{"name": "activeUsers"}, {"name": "totalUsers"}, {"name": "newUsers"}, {"name": "active1DayUsers"}, {"name": "screenPageViews"}, 
    #         {"name": "averageSessionDuration"}, {"name": "eventCount"}, {"name": "sessions"}, {"name": "screenPageViews"}],
    #     date_ranges=[{"start_date": "2020-01-01", "end_date": "today"}]  # As an example, pulling data from 2020 to today
    # )
    #     request2 = RunReportRequest(
    #     property=f"properties/{PROPERTY_ID}",
    #     dimensions=[
    #         {"name": "country"}
    #     ],
    #     metrics=[ {"name": "totalUsers"} ]
    # )
    #         request3 = RunReportRequest(
    #     property=f"properties/{PROPERTY_ID}",
    #     dimensions=[
    #         {"name": "browser"}
    #     ],
    #     metrics=[ {"name": "totalUsers"} ]
    # )
    #         request4 = RunReportRequest(
    #     property=f"properties/{PROPERTY_ID}",
    #     dimensions=[
    #         {"name": "os"}
    #     ],
    #     metrics=[ {"name": "totalUsers"} ]
    # )
    

    # batch_request = BatchRunReportsRequest(
    #     property=f"properties/{PROPERTY_ID}",
    #     requests=[request1, request2, request3, request4]
    # )
    
    # # Call the API to fetch the batch report
    # response = client.batch_run_reports(batch_request)
    
    #         # Aggregate data into a single document
    # aggregate_data = {
    # 'Date': datetime.utcnow().strftime('%Y-%m-%d'),  # Use current date as a unique key for this report
    # 'Details': []
    # }

    # for row in response.rows:
    #     detail = {
    #         'Date': row.dimension_values[0].value,
    #         'ActiveUsers': int(row.metric_values[0].value),
    #         'TotalUsers': int(row.metric_values[1].value),
    #         'NewUsers': int(row.metric_values[2].value),
    #         'Active1DayUsers': int(row.metric_values[3].value),
    #         'PageViews': int(row.metric_values[4].value),
    #         'AvgSessionDuration': Decimal(str(row.metric_values[5].value))
    #     }
    #     aggregate_data['Details'].append(detail)
    
    # # Write the aggregated data to DynamoDB
    # table.put_item(Item=aggregate_data)

    
    # Write data to DynamoDB
    # with table.batch_writer() as batch:
    #     for item in items:
    #         batch.put_item(Item=item)


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
