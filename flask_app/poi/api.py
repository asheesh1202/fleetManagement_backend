from flask import Blueprint, json , request
from init import db
poiBp =Blueprint('poiBp', __name__)

@poiBp.route('/add/', methods=['POST'])
def add_poi():
    #check if the form is valid 
    if request.method == 'POST':
        name = request.form['name']
        lat = request.form['lat']
        lng = request.form['lng']
       # region = 
        address = request.form['address']
        category = request.form['category']
        point = {
            "name": name,
            "lat" : lat,
            "lng" : lng,
            "category":category,
            "address":address
        }
        db.poi.insert_one(school)
	return {'result':'poi added'}

@poiBp.route('/get_all/', methods = ['GET'])
def get_allPOI():
    allPois  = db.poi.find()
    res={}
    i = 0
    for poi in allPois: 
        res[i] = poi
        i+=i
        
    response = json.dumps(res, indent = 4)
    return response

@poiBp.route('/get/', methods=['GET'])
def getPoi( ):
    searchRes = db.poi.find_one({'name':request.form['name']})
    response = {
    'name': searchRes['name'],
    'lat' : searchRes['lat'],
    'lng' : searchRes['lng'],
    #'region' = searchRes['region']
    'address' : searchRes['address'],
    'category' : searchRes['category']
    }
    return response
    
@poiBp.route('/update/', methods=['Update'])
def updatePoi( ):
    searchRes = db.poi.find_one({'name':request.form['name']})
    #things to update
    #opens update form 
    
    if searchRes:
        users_drivers.find_one_and_update({  'name':request.form['name']},
                                      { '$set': {'name': request.form['lat'],
                                                  'lat': request.form['lng'], 
                                                  'lng': request.form['lng'],
                                                  'category': request.form['category'],
                                                  'region': request.form['region'],
                                                  'address': request.form['address']}
                                      }, 
                                      upsert=False)
    return 'true/successful'
    
@poiBp.route('/delete/' ,methods = ['DELETE'])
def deletePoi(  ):
    delete = db.poi.delete ({'name':request.form['name']})
    
