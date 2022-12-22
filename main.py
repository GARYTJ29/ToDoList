from flask import Flask, jsonify, request, redirect, render_template, url_for, make_response, session
from flask.helpers import url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,jwt_required,get_jwt_identity
)
import json
from pymongo import MongoClient
import bson.json_util as json_util
from bson import ObjectId
from flask_session import Session
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

from routers.pages import pagesRouter
from routers.tasks import taskRouter
from routers.users import userRouter

app = Flask(__name__)
app.config.from_object(__name__)

client = MongoClient('mongodb+srv://madhav:qjPrL48Kwa6kBKf2@flask-todo.y66rx9x.mongodb.net/?retryWrites=true&w=majority')
tasksDB=client.tasks
usersDB=client.users

app.config['CORS_Headers'] = 'Content-Type'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.secret_key="top_secret"
app.config['SECRET_KEY'] = 'super-secret'
app.config['secret_key'] = 'super-secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Bootstrap(app)
datepicker(app)
cors = CORS(app)
sess = Session()
sess.init_app(app)
jwt = JWTManager(app)

# if u get cross origin error then use the below method before the router function
# @cross_origin()
@app.route("/tasks")
@jwt_required()
def home():
    tokenData=get_jwt_identity()
    user = json.loads(tokenData)
    holder = list()
    currentCollection = tasksDB.tasks
    k=1
    err = session.get("errortask","")
    session["errortask"]=""
    for i in currentCollection.find({"owner":user.get("email","")}):
        i['num'] = k
        k+=1
        holder.append(i)
    return render_template("base.html",taskdata = holder,err=err)

pagesRouter(app,tasksDB)
taskRouter(app,tasksDB)
userRouter(app,usersDB)


if __name__ == '__main__':
    app.run(debug = True)