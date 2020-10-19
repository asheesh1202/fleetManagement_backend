from flask import Blueprint, json , request, make_response
import models
from init import db, users_drivers, client
userBp = Blueprint('userBp', __name__)


@userBp.route('/')
def getAllUsers():
    allUsers = db.users_drivers.find()
    print()
    resp ={}
    for user in allUsers:

	resp[str(user['_id'])] = {"username" : user['username'], 
				 "category": user['category']
				 }
    return json.dumps(resp)

@userBp.route('/delete')
def deleteDb():
    client.drop_database('db')
    db = client.db
    return 'delete and clreated'
@userBp.route('/addUser/', methods=['POST']) #usage users/addusers/driver/ #body
def adUser():
    userDetails = {
	'username' : request.get_json()['username'],
	'password' : request.get_json()['password'],
  	'category' : request.get_json()['category'],
        'currentLat': 0.0,
	'currentLng': 0.0
	}
    print(request.get_json())
    #if not db.users_drivers.find({'username': request.form['username']}) or not db.users_operators.find({'username': request.form['username']}):	
    if request.get_json()['category'] == 'Driver':
	db.users_drivers.insert_one(userDetails)
    #elif category == 'Operator':
	#db.users_operators.insert_one(userDetails)
    return {'result': 'new user successfully added'}
    #return {'result':'user with same username already exists'}
	

@userBp.route('/deleteUser/<category>', methods=['DELETE'])
def deleteUser(category):
    if category == 'driver':
	if db.users_drivers.find_one({email:request.form['username']}):
	        db.user_drivers.delete_one({email:request.form['username']})
	else: return {'result': 'user donot exists'}
    elif category == 'operator':
	if db.users_operators.find_one({email:request.form['username']}):
	        db.users_operators.delete_one({email:request.form['username']})	
	else: return {'result': 'user donot exists'}

@userBp.route("/updateCurrentLocation/", methods=['POST'])
def update_current_location():
    if request.method == 'POST':
        if users_drivers.find_one({'username':request.get_json()['username']})!=None:
            id = users_drivers.find_one({'username':request.get_json()['username']})['_id']
            print(id)
            users_drivers.find_one_and_update({ 'username': request.get_json()['username'] },
                                      { '$set': {'currentLat': request.get_json()['currentLat'],
                                                  'currentLng': request.get_json()['currentLng'] }
                                      }, 
                                       upsert=False)
            return {'result':'location updated'}
        else:
            return {'result':'user not found'}


@userBp.route("/get_current_location/", methods=['GET','POST'])
def get_current_location():
    if request.method =='GET' or request.method =='POST':
	print(request.get_json()['username'])
        if users_drivers.find_one({'username':request.get_json()['username']})!=None:
            lat  = users_drivers.find_one({'username':request.get_json()['username']})['currentLat']
            lng  = users_drivers.find_one({'username':request.get_json()['username']})['currentLng']
            if lat != 0 and lng != 0:   
                res = {
                        'lat':lat,
                        'lng':lng,
                        'username':request.get_json()['username']
                      
                        }
                return make_response(res, 200) 
            else:
                return {'result':'invalid lat lng'}
        else: 
            return {'result':'invalid user'}
