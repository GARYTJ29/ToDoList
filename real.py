from flask import Flask, jsonify, request, redirect, render_template, url_for, make_response, session
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
from bson import ObjectId
from flask_session import Session

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
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
jwt = JWTManager(app)

# if u get cross origin error then use the below method before the router function
# @cross_origin()


#users router below


@app.route("/")
def login():
    return render_template("login.html",signup=False,error = session.get("errorLogin",[[],[]]))
@app.route("/tasks")
@jwt_required()
def home():
    tokenData=get_jwt_identity()
    user = json.loads(tokenData)
    holder = list()
    currentCollection = tasksDB.tasks
    k=1
    for i in currentCollection.find({"owner":user.get("email","")}):
        i['num'] = k
        k+=1
        holder.append(i)
    return render_template("base.html",taskdata = holder)
@app.route("/signup")
def signup():
    return render_template("login.html",signup=True, error = session.get("errorLogin",[[],[]]))
    
@app.route("/update/<id>")
@jwt_required()
def update(id):
    currentCollection = tasksDB.tasks
    oid = ObjectId(id)
    k=1
    for i in currentCollection.find({'_id':oid}):
        a=i
    return render_template("Task.html", a = a)


@app.route('/signupapi', methods = ['POST'])
def signupapi():
    
    currentCollection = usersDB.users
    # name = request.json['name']
    # email = request.json['email']
    name = request.form.get("name")
    email = request.form.get("email") 

    data = currentCollection.find_one({"email" : email})
    if data:
        session["errorLogin"]=[[],["user already  exists"]]
        return redirect(url_for('signup'))
    password = generate_password_hash(request.form.get("password"), method='sha256')
    currentCollection.insert_one({'name' : name, 'email' : email, 'password' : password})
   
    user=json.dumps({'name' : name, 'email' :email})

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    # Set the JWT cookies in the response
    resp = jsonify({'signup': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    #return {'signup': True}, 200
    return redirect(url_for('login'))

@app.route('/loginapi', methods=['POST'])
def loginapi():
    email = request.form.get("email")
    password = request.form.get("password")
    currentCollection = usersDB.users
    data = currentCollection.find_one({"email" : email})
    if not data:
        session["errorLogin"]=[["User not found"],[]]
        return redirect(url_for("login"))
    if not check_password_hash(data["password"],password):
        session["errorLogin"]=[["Incorrect Password"],[]]
        return redirect(url_for("login"))
    user=json.dumps({'name' : data['name'], 'email' : data['email']})

    # Create the tokens we will be sending back to the user
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    # Set the JWT cookies in the response
    resp = jsonify({'login': True})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    response = make_response(redirect(url_for("home")))
    response.set_cookie('access_token_cookie', access_token)
    response.set_cookie('refresh_token_cookie', refresh_token)
    return response

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


@app.route('/logout')
def logout():
    resp = redirect(url_for("login"))
    unset_jwt_cookies(resp)
    return resp

#tasks rotuer below
@app.route('/tasksapi', methods = ['GET'])
@jwt_required()
def retrieveAllTasks():
    tokenData=get_jwt_identity()
    user = json.loads(tokenData)
    holder = list()
    currentCollection = tasksDB.tasks
    for i in currentCollection.find({"owner":user.get("email","")}):
        holder.append(i)
    return json_util.dumps(holder)

@app.route('/tasksapi', methods = ['POST'])
@jwt_required()
def addTask():
    tokenData=get_jwt_identity()
    user = json.loads(tokenData)
    owner = user.get("email","none")
    currentCollection = tasksDB.tasks
    task = request.form.get("title")
    currentCollection.insert_one({'owner' : owner, "task":task})
    resp = jsonify({'created': True})

    return redirect(url_for("home"))

@app.route('/deleteTask/<id>')
def deleteData(id):
    oid = ObjectId(id)
    currentCollection = tasksDB.tasks
    currentCollection.delete_one({'_id' : oid})
    return redirect(url_for('home'))

@app.route('/updateTask/<id>', methods = ['PUT'])
def updateData(id):
    currentCollection = tasksDB.tasks
    oid = ObjectId(id)
    task = request.form.get("title")
    currentCollection.update_one({'_id':oid}, {"$set" : {'task' : task}})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)