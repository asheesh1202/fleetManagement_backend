from flask import Flask, request, make_response, g
import config
app =Flask(__name__)
import pymongo
client = pymongo.MongoClient(config.DevelopementConfig.MONGODBURI)

import os 
import sys
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


db = client.db
users_drivers = db.users_drivers
            


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 
