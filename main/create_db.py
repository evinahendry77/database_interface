#!/bin/python3
# Program name: create_db.py
# Creator: Evin Hendry
# Date created: December 7th, 2020
# Purpose: Creates a table named "Clients" in AWS's Dynamodb, using Boto3.
from __future__ import print_function
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

# Change the table name and its attributes as you see fit. 

def create_clients_table():
    table = dynamodb.create_table(
        TableName='Clients',
        KeySchema=[
            {
                'AttributeName': 'ClientID',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ClientID',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
    print("Table status: ", table.table_status)
    print("Clients table created.")

create_clients_table()
