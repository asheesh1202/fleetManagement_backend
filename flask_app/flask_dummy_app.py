from flask import Blueprint, json , request, Flask 


app = Flask(__name__)


@app.route('/')
def getAllUsers():
    return 'you are able to access the my system'
