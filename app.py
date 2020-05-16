from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import *

import requests
import json

from config import *
from helper import *
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']=get_secret_key()
app.config['JWT_SECERET_KEY']=get_jwt_secret_key()

db = SQLAlchemy(app)

jwt = JWTManager(app)

def get_db():
    return db

@app.route('/')
def hello():
    return "Hello World!"
    
@app.route('/register',methods=['POST'])
def register():
    data = request.json
    req_str = get_api_str() 
    req_str += "clients/"
    key = get_branch_key()
    
    email = data["user"]["email"]
    password = data["user"]["password"]
    if User.find_email(email):
        return {'message': 'Email {} already exists'. format(email)}
    new_user = User(
        email = email,
        password = User.generate_hash(password)
    )

    data.pop('user', None)

    try:
        new_user.save_to_db()
        access_token = create_access_token(identity = email)
        refresh_token = create_refresh_token(identity= email)
        data["client"]["assignedBranchKey"] = key
        headers = {"Accept":"application/json"}
        req = requests.post(req_str, auth=(get_mambu_user(),get_mambu_pw()), json=data, headers=headers)
        req_data = req.json()

        if "returnCode" in req_data:
            return "error"
        
        new_user_profile = UserProfile(
            userid = new_user.find_email(email).id,
            mambuid = req_data['client']['id'],
            encodedkey= req_data['client']['encodedKey'],
            firstname = req_data['client']['firstName'],
            lastname = req_data['client']['lastName'],
            clientrolekey = req_data['client']['clientRole']['encodedKey']
        )

        new_user_profile.save_to_db()

        return {
            'message': 'User was successfully created',
            'access_token': access_token,
            'refresh_tokem': refresh_token
        }
    except:
        return {'message':"Something went wrong"}

@app.route('/login',methods=['POST'])
def login():
    data = request.json
    email = data["email"]
    password =data["password"]

    current_user = User.find_email(email)
    if not current_user:
        return {'message': 'Email {} doesn\'t exist'.format(email)}

    if User.verify_hash(password,current_user.password):
        access_token = create_access_token(identity = email)
        refresh_token = create_refresh_token(identity = email)
        return {
            'message': 'User is Logged in',
            'access_token': access_token,
            'refresh_token': refresh_token
            }
    else:
        return {'message': 'Wrong credentials'}


if __name__ == '__main__':
    app.run()