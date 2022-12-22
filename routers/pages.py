from flask import Flask,  render_template,  session
from flask_jwt_extended import (
    JWTManager, jwt_required, 
    get_jwt_identity, 
)
import json
import bson.json_util as json_util
from bson import ObjectId
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
# if u get cross origin error then use the below method before the router function
# @cross_origin()


#pages routes below

def pagesRouter(app,tasksDB):
    @app.route("/")
    def login():
        return render_template("login.html",signup=False,error = session.get("errorLogin",[[],[]]))

    

    @app.route("/signup")
    def signup():
        return render_template("login.html",signup=True, error = session.get("errorLogin",[[],[]]))
        
    @app.route("/update/<id>")
    @jwt_required()
    def update(id):
        currentCollection = tasksDB.tasks
        oid = ObjectId(id)
        k=1
        err = session.get("errortask","")
        
        for i in currentCollection.find({'_id':oid}):
            a=i
        return render_template("Task.html", a = a,err=err)