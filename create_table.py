
from __future__ import print_function
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='push',
    KeySchema=[
        {
            'AttributeName': 'push_id',
            'KeyType': 'HASH'  #Partition key
        },

    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'push_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'karma',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Table status:", table.table_status)
