from flask import Flask
from flask import jsonify
from flask import request
import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')

@app.route('/', methods=['GET'])
def get_all_ips():
    table = dynamodb.Table('ips')
    response = table.scan()
    return jsonify({'result' : response['Items']})

@app.route('/<ip>', methods=['GET'])
def get_one_ip(ip):
    table = dynamodb.Table('ips')
    response = table.query(KeyConditionExpression=Key('ip').eq(ip+'/32'))
    print response['Items']
    return jsonify({'result' : response['Items']})

@app.route('/service/<service>', methods=['GET'])
def get_service_ips(service):
    table = dynamodb.Table('ips')
    response = table.scan(
        FilterExpression=Attr('service').eq(service)
    )
    return jsonify({'result' : response['Items']})

@app.route('/', methods=['POST'])
def add_ip():
    table = dynamodb.Table('ips')
    ip = request.json['ip']
    service = request.json['service']
    ip_exists = table.query(KeyConditionExpression=Key('ip').eq(ip))
    if ip_exists['Count'] != 0:
        return jsonify({'ip-exist' : ip})
    #insert-ip
    response = table.put_item(Item =  {'ip': ip,'service': service})
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        result = {'ip' : ip, 'service' : service}
    return jsonify({'result' : result})

@app.route('/ips/delete', methods=['POST'])
def delete_one_ip():
    table = dynamodb.Table('ips')
    ip = request.json['ip']
    ip_exists = table.query(KeyConditionExpression=Key('ip').eq(ip))
    if ip_exists['Count'] == 0:
        return jsonify({'ip-non-exist' : ip})
    #delte-ip
    response = table.delete_item(Key = {'ip': ip})
    print response
    return {"ip deleted" : ip}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
