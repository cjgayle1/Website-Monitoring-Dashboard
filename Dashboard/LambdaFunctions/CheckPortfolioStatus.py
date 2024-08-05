import boto3
import time
from datetime import datetime
import urllib.request
from decimal import Decimal


def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-2')
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    
    # wesbitemonitoring is mispelled don't forget
    table = dynamodb.Table('WesbiteMonitoring')
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-2:400439970044:WebsiteDownAlert'

    url = 'https://christopher-gayle.com/'
    start_time = time.time()
    try:
        response = urllib.request.urlopen(url)
        latency = time.time() - start_time
        data = response.read()
        
        latency_decimal = Decimal(str(latency))

        table.put_item(
            Item={
                'URL': url,
                'DateTimeCheck': datetime.utcnow().isoformat(),
                'StatusCode': response.getcode(),
                'ResponseTime': latency_decimal
            }
        )
        cloudwatch.put_metric_data(
            Namespace='WebsiteMonitoring',
            MetricData=[
                {
                    'MetricName': 'ResponseTime',
                    'Dimensions': [
                        {'Name': 'URL', 'Value': url}
                    ],
                    'Unit': 'Seconds',
                    'Value': latency
                },
                {
                    'MetricName': 'StatusCode',
                    'Dimensions': [
                        {'Name': 'URL', 'Value': url}
                    ],
                    'Unit': 'Count',
                    'Value': response.getcode()
                }
            ]
        )
        return {
            'statusCode': response.getcode(),
            'data': str(data)
        }
    except Exception as e:
        sns.publish(
            TopicArn=topic_arn,
            Message=f'Alert: The website {url} is down due to {str(e)}.',
            Subject='Website Down Alert'
        )
        return {
            'statusCode': 503,
            'error': str(e)
        }
