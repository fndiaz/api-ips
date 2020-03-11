from flask import Flask
from flask import jsonify
from flask import request
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("ips")
token = os.getenv("token")


@app.route("/", methods=["GET"])
def get_all_ips():
    response = table.scan()
    result = sorted(response["Items"], key=lambda x: x["service"], reverse=False)
    return jsonify({"result": result})


@app.route("/<ip>", methods=["GET"])
def get_one_ip(ip):
    response = table.query(KeyConditionExpression=Key("ip").eq(ip + "/32"))
    return jsonify({"result": response["Items"]})


@app.route("/service/<service>", methods=["GET"])
def get_service_ips(service):
    response = table.scan(FilterExpression=Attr("service").eq(service))
    return jsonify({"result": response["Items"]})


@app.route("/", methods=["POST"])
def add_ip():
    if check_json(request.json) is False:
        return "Malformed", 400
    ip = request.json["ip"]
    service = request.json["service"]
    ip_exists = table.query(KeyConditionExpression=Key("ip").eq(ip))
    if ip_exists["Count"] != 0:
        return jsonify({"ip-exist": ip})
    # insert-ip
    response = table.put_item(Item={"ip": ip, "service": service})
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        result = {"ip": ip, "service": service}
    return jsonify({"result": result})


@app.route("/delete", methods=["POST"])
def delete_one_ip():
    if check_json(request.json) is False:
        return "Malformed", 400
    ip = request.json["ip"]
    ip_exists = table.query(KeyConditionExpression=Key("ip").eq(ip))
    if ip_exists["Count"] == 0:
        return jsonify({"ip-non-exist": ip})
    # delte-ip
    table.delete_item(Key={"ip": ip})
    return {"ip deleted": ip}


def check_json(var):
    try:
        var["ip"]
        var["service"]
        token_post = var["token"]
    except:
        return False
    if token_post != token:
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
