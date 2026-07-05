import json
import os
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    http_method = event.get('httpMethod')
    
    if http_method == 'GET':
        response = table.scan()
        items = response.get('Items', [])
        resources = []
        for item in items:
            if item.get('PK', '').startswith('RESOURCE#'):
                resources.append({
                    'id': item['PK'].split('#')[1],
                    'name': item.get('name', 'Unknown'),
                    'type': item.get('type', 'Unknown'),
                    'status': item.get('status', 'Unknown'),
                    'capacity': int(item.get('capacity', 0)),
                    # Convert back to float for the frontend map
                    'lat': float(item.get('lat', 0)),
                    'lng': float(item.get('lng', 0))
                })
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(resources)
        }
    
    elif http_method == 'POST':
        body = json.loads(event['body'])
        resource_id = body.get('id', datetime.now().isoformat())
        
        table.put_item(Item={
            'PK': f"RESOURCE#{resource_id}",
            'SK': f"METADATA#{resource_id}",
            'name': str(body['name']),
            'type': str(body['type']),
            'status': str(body['status']),
            'capacity': int(body['capacity']),
            # MUST CONVERT TO STRING FOR DYNAMODB (Fixes 502 Bad Gateway)
            'lat': str(body['lat']),
            'lng': str(body['lng'])
        })
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({'message': 'Resource created successfully'})
        }
        
    return {
        'statusCode': 400,
        'headers': headers,
        'body': json.dumps({'error': 'Unsupported method'})
    }
