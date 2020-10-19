from flask import Blueprint, json , request
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
@userBp.route('/addUser/<category>', methods=['POST']) #usage users/addusers/driver/ #body
def adUser(category):
    userDetails = {
	'username' : request.form['username'],
	'password' : request.form['password'],
  	'category' : request.form['category'],
        'currentLat': 0.0,
	'currentLng': 0.0
	}

    if not db.users_drivers.find({'username': request.form['username']}) or not db.users_operators.find({'username': request.form['username']}):	
        if category == 'driver':
	    db.users_drivers.insert_one(userDetails)
        elif category == 'operator':
	    db.users_operators.insert_one(userDetails)
	return {'result': 'new user successfully added'}
    return {'result':'user with same username already exists'}
	

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

@userBp.route("/update_current_location/", methods=['POST'])
def update_current_location():
    if request.method == 'POST':
        if users_drivers.find_one({'username':request.form['username']})!=None:
            id = users_drivers.find_one({'username':request.form['username']})['_id']
            print(id)
            users_drivers.find_one_and_update({ 'username': request.form['username'] },
                                      { '$set': {'lat': request.form['lat'],
                                                  'lng': request.form['lng'] }
                                      }, 
                                       upsert=False)
            return {'result':'location updated'}
        else:
            return {'result':'user not found'}


@userBp.route("/get_current_location/", methods=['GET'])
def get_current_location(username):
    if request.method =='GET':
        if users_drivers.find_one({'username':request.form['username']})!=None:
            lat  = users_drivers.find_one({'username':request.form['username']})['lat']
            lng  = users_drivers.find_one({'username':request.form['username']})['lng']
            if lat != 0 and lng != 0:   
                res = {
                        'lat':lat,
                        'lng':lng,
                        'username':username
                      
                        }
                return make_response(res, 200) 
            else:
                return {'result':'invalid lat lng'}
        else: 
            return {'result':'invalid user'}
