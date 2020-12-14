#!/bin/python3
# Program name: main.py
# Creator: Evin Hendry
# Date created: December 12th, 2020
# Purpose: See "user_guide.txt"

from __future__ import print_function
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# Prints the results. Dynamodb automatically presents its
# data in JSON format. This class makes it more readable.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def display_menu(text):
    # Initial user menu.
    print("""\nOptions:
0. VIEW HELP DOCUMENTATION.
1. View a client's information.
2. Print all clients' information with keys identified.
3. Enter a new client's information in the database.
4. Remove a client from the database.
5. Display all statements inside the storage bucket.
6. Download a statement from a storage bucket to the local system.
7. Upload a statement from the local system to a storage bucket.
8. Delete a statement from the storage bucket.
9. Exit.""")

# Input validation clause. If the user attempts to insert a
# non-numerical value, an error message is displayed.
# This is useful for preventing injection-based attacks.  
    while True:
        try:
            user_int = int(input(text))
            return user_int
        except ValueError:
            print("ERROR: Select one of the options listed above.")


def display_manual():
    print("""\nWelcome to the company's internal database interface. This
program allows you to directly interact with the database and a storage unit
intended for client statements.

To use this program, utilize the number keys on your keyboard as instructed by
the menu.

All client information belongs in the database, as indicated by options 1-4.

All business statements for transactions belong in the storage bucket, as
indicated by options 5-8.

Press "9" to exit the program.""")


def display_client_info():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Clients')

    item_key = int(input("\nEnter a client's ID number: "))
    response = table.query(
        KeyConditionExpression=Key('ClientID').eq(item_key)
    )
    for i in response['Items']:
        print(json.dumps(i, cls=DecimalEncoder))


def display_all_clients():
    dynamodb = boto3.client('dynamodb')

    response = dynamodb.scan(
       TableName = 'Clients',
       Select = 'ALL_ATTRIBUTES')
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(
        TableName = 'Clients',
        Select = 'ALL_ATTRIBUTES',
        ExclusiveStartKey=response['LastEvaluatedKey']
            )
        data.extend(response['Items'])
    for i in response['Items']:
        print(json.dumps(i, cls=DecimalEncoder))


def enter_client_info():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Clients')

    client_id_no = int(input("\nEnter a unique, 5-digit ID for your client: "))
    # Potential input vulnerabilities, assess best SQL mitigation solution.
    business_name = input("Enter the client's business name: ")
    point_of_contact = input("Enter the point of contact's full name: ")
    poc_email = input("Enter the point of contact's e-mail address: ")
    poc_number = input("Enter the point of contact's phone number: ")

    client_data = [[client_id_no, business_name, point_of_contact, poc_email, poc_number]]

    for client in client_data:
        id_no = client[0]
        name = client[1]
        poc = client[2]
        email = client[3]
        number = client[4]

    table.put_item(
        Item={
            'ClientID' : id_no,
            'Client Name' : name,
            'Point of Contact' : poc,
            'E-mail' : email,
            'Phone Number' : number
        }
    )

    print("\nClient [" + business_name + "] successfully uploaded to database. Key number: " + str(client_id_no))


def remove_client_info():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Clients')

    id_number = int(input("Enter a client ID key: "))
    try:
        response = table.delete_item(
            Key={
                'ClientID' : id_number
            },
        )
        print("Client information removed.")
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response


def display_statements():
    s3 = boto3.resource('s3')

    print("\nCURRENT STATEMENTS: \n")

    # Reference the bucket you created here. Same deal, fully qualified domain name.
    # Make sure it's in quotation marks.

    my_bucket = s3.Bucket(YOUR_BUCKET_HERE)

    for file in my_bucket.objects.all():
        print(file.key)


def download_statement():
    s3 = boto3.resource('s3')

    # Your bucket here, again.

    statements_bucket = YOUR_BUCKET_HERE
    KEY = input("\nEnter the name of the statement you wish to download: ")
    file_name = KEY

    try:
        s3.Bucket(statements_bucket).download_file(KEY, file_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def upload_statement():
    s3 = boto3.client('s3')

    filename = input("\nEnter a file name: ")

    # Your bucket here, again.

    bucket_name = YOUR_BUCKET_HERE
    s3.upload_file(filename, bucket_name, filename)


def delete_statement():
    s3 = boto3.resource("s3")

    statement = input("\nEnter the name of the statement to delete: ")

    # You get the idea.

    obj = s3.Object(YOUR_BUCKET_HERE, statement)
    obj.delete()


def menu_selection(message):
    USER_INPUT = display_menu("\nSelect an option: ")
    while USER_INPUT != 9:
        if USER_INPUT == 0:
            display_manual()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 1:
            display_client_info()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 2:
            display_all_clients()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 3:
            enter_client_info()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 4:
            remove_client_info()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 5:
            display_statements()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 6:
            download_statement()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 7:
            upload_statement()
            USER_INPUT = display_menu("\nSelect another option: ")

        elif USER_INPUT == 8:
            delete_statement()
            USER_INPUT = display_menu("\nSelect another option: ")

        else:
            print("\nERROR: Select one of the options listed above.")
            USER_INPUT == display_menu("")


def mainframe():
    menu_selection("Welcome to the client database, administrator. Select from the menu to get started.")
    print("Thank you!")

mainframe()
