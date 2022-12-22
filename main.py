from flask import Flask, jsonify, request, redirect, render_template, url_for, make_response, session
from flask.helpers import url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,\
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

Bootstrap(app)
datepicker(app)
cors = CORS(app)
Session(app)
jwt = JWTManager(app)

client = MongoClient('mongodb+srv://madhav:qjPrL48Kwa6kBKf2@flask-todo.y66rx9x.mongodb.net/?retryWrites=true&w=majority')
tasksDB=client.tasks
usersDB=client.users

app.config['CORS_Headers'] = 'Content-Type'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'
app.config['secret_key'] = 'super-secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"



# if u get cross origin error then use the below method before the router function
# @cross_origin()


pagesRouter(app,tasksDB)
taskRouter(app,tasksDB)
userRouter(app,usersDB)


if __name__ == '__main__':
    app.run(debug = True)