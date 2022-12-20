from flask import Flask, jsonify, request, redirect
from flask.helpers import url_for
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import json
from pymongo import MongoClient
import bson.json_util as json_util

client = MongoClient('mongodb+srv://madhav:qjPrL48Kwa6kBKf2@flask-todo.y66rx9x.mongodb.net/?retryWrites=true&w=majority')
tasksDB=client.tasks
usersDB=client.users

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_Headers'] = 'Content-Type'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

# if u get cross origin error then use the below method before the router function
# @cross_origin()


#users router below

@app.route('/signUp', methods = ['POST'])
def signUp():
    
    currentCollection = usersDB.users
    name = request.json['name']
    email = request.json['email']
    data = currentCollection.find_one({"email" : email})
    if data:
        return jsonify({'signup': False,"error":"user already  exists"}), 400
    password = generate_password_hash(request.json['password'], method='sha256')
    currentCollection.insert_one({'name' : name, 'email' : email, 'password' : password})
   
    user=json.dumps({'name' : name, 'email' :email})

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    # Set the JWT cookies in the response
    resp = jsonify({'signup': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return {'signup': True}, 200

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    currentCollection = usersDB.users
    data = currentCollection.find_one({"email" : email})
    if not data or not check_password_hash(data["password"],password):
        return jsonify({'login': False}), 401
    user=json.dumps({'name' : data['name'], 'email' : data['email']})

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    # Set the JWT cookies in the response
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

# Same thing as login here, except we are only setting a new cookie
# for the access token.
# @app.route('/token/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     # Create the new access token
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)

#     # Set the JWT access cookie in the response
#     resp = jsonify({'refresh': True})
#     set_access_cookies(resp, access_token)
#     return resp, 200


@app.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

#tasks rotuer below
@app.route('/tasks', methods = ['GET'])
@jwt_required()
def retrieveAllTasks():
    tokenData=get_jwt_identity()
    user = json.loads(tokenData)
    holder = list()
    currentCollection = tasksDB.tasks
    for i in currentCollection.find({"owner":user.get("email","")}):
        holder.append(i)
    return json_util.dumps(holder)

@app.route('/task', methods = ['POST'])
@jwt_required()
def addTask():
    tokenData=get_jwt_identity()
    user = json.loads(tokenData)
    owner = user.get("email","none")

    currentCollection = tasksDB.tasks
    task = request.json['task']
    currentCollection.insert_one({'owner' : owner, "task":task})
    resp = jsonify({'created': True})

    return resp, 200

@app.route('/deleteTask/<id>', methods = ['DELETE'])
def deleteData(id):
    currentCollection = tasksDB.tasks
    currentCollection.delete_one({'_id' : id})
    return redirect(url_for('retrieveAll'))

@app.route('/updateTask/<id>', methods = ['PUT'])
def updateData(id):
    currentCollection = tasksDB.tasks
    task = request.json['task']
    currentCollection.update_one({'_id':id}, {"$set" : {'task' : task}})
    return redirect(url_for('retrieveAll'))

if __name__ == '__main__':
    app.run(debug = True)