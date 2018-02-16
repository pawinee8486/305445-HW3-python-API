import pymongo
from datetime import datetime , date
from flask import Flask,request
from flask_restful import Resource , Api , reqparse
import json


#url to access mongodb
# "momgodb://[username]:[password]@localhost:[port]/[name_db]
url = "mongodb://mumu:1234@localhost:27017/admin"
client = pymongo.MongoClient(url)
#db = client.admin.network_system
db = client.admin.cpe_company_limited
#print db.name

#init Flask
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('information')

class Registration(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		db.update_one({"id":data['id']},
			{'$set':
			{"id":data['id'],"firstname":data['firstname'],"lastname":data['lastname'],"password":data['password']}
			},upsert= True
			)
		print(data)
		return {'id':data['id'],'firstname':data['firstname'],"lastname":data['lastname'],"password":data['password']}

class Login(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		login_datetime = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
		db.update_one({"id":data['id']},
			{'$push':
			{"list_work":{"datetime":login_datetime}}})
		result = db.find_one({'id':data['id']})
		print result
		return {'firstname':result['firstname'],'list_work':login_datetime}

class History(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		result = db.find_one({'id':data['id']})
		return {'firstname':result['firstname'],'listdate':result['listdate']}

api.add_resource(Registration,'/api/register')
api.add_resource(Login,'/api/login')
api.add_resource(History,'/api/history_work')


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5001)


