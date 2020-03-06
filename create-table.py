import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def create_table():
    """
    This function creates a table in dynamodb
    Returns
    -------
    String
        table creation status string
    """
    table = dynamodb.create_table(
        TableName='Movies',
    KeySchema=[
        {
            'AttributeName': 'year',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'title',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'year',
            'AttributeType': 'N'
        },
        {
            'AttributeName': 'title',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
    )
    return table.table_status

def insert_data():
    """
    This function inserts data in dynamodb table
    Returns
    -------
    Dictionary
        Response Dictionary
    """
    table = dynamodb.Table('ips') 
    #with put_item function we insert data in Table
    response = table.put_item(
        Item = {
               'ip': '1.1.1.1/32',
               'service': 'campinas'  
               }
        )
    return response

#print insert_data()

def get_data():
    """
    This function reads data from dynamodb table
    Returns
    -------
    
        Response Dictionary
    """
    table = dynamodb.Table('ips')
    #with Get_item function we get the data
    response = table.get_item(
        Key = {
               'ip': '8.8.8.8/32'
               }
        )
    return response['Item']

#print get_data()

def get_service():
    """
    This function reads data from dynamodb table
    Returns
    -------
    
        Response Dictionary
    """
    table = dynamodb.Table('ips')
    #with Get_item function we get the data
    response = table.scan(FilterExpression=Attr('service').eq('campinas'))
    return response['Items']

print get_service()

def delete_data():
    """
    This function delete data from dynamodb table
    Returns
    -------
    
        Response Dictionary
    """
    table = dynamodb.Table('ips')
    #with delete_item function we delete the data from table
    response = table.delete_item(
        Key = {
               'ip': '8.8.8.9/32'
               }
        )
    return response

#print delete_data()