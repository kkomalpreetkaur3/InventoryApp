import json
import boto3
import os
import ulid
from decimal import Decimal


def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }
    except Exception:
        return {
            'statusCode': 400,
            'body': json.dumps("Invalid JSON format.")
        }

    # Get table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Generate a unique ULID
    unique_id = str(ulid.new())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'location_id': int(data['location_id']),
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty_on_hand': int(data['item_qty_on_hand']),
                'item_price': Decimal(str(data['item_price']))
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing required field: {str(e)}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }