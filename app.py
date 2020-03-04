from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'ipscoll'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ipscoll'

mongo = PyMongo(app)

@app.route('/ips', methods=['GET'])
def get_all_ips():
  ips = mongo.db.ips
  output = []
  for s in ips.find():
    output.append({'ip' : s['ip'], 'service' : s['service']})
  return jsonify({'result' : output})

@app.route('/ips/service/<service>', methods=['GET'])
def get_one_ip(service):
  ips = mongo.db.ips
  output = []
  s = ips.find({'service' : service})
  for dado in s:
    output.append({'ip' : dado['ip'], 'service' : dado['service']})
  return jsonify({'result' : output})

@app.route('/ips', methods=['POST'])
def add_ip():
  ips = mongo.db.ips
  ip = request.json['ip']
  if ips.find_one({'ip': ip }):
    return jsonify({'ip-exist' : ip})
  service = request.json['service']
  ip_id = ips.insert({'ip': ip, 'service': service})
  new_ip = ips.find_one({'_id': ip_id })
  output = {'name' : new_ip['ip'], 'service' : new_ip['service']}
  return jsonify({'result' : output})

@app.route('/ips/delete', methods=['POST'])
def delete_one_ip():
  ips = mongo.db.ips
  ip_del = request.json['ip']
  print ip_del
  myquery = { "ip":  ip_del }
  res = ips.delete_many(myquery)
  print res.deleted_count
  return {"documents deleted" : res.deleted_count}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
