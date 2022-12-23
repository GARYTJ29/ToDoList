from flask import  render_template,  session
from flask_jwt_extended import (
 jwt_required, 
    get_jwt_identity, 
)
import json
from bson import ObjectId
# if u get cross origin error then use the below method before the router function
# @cross_origin()

priorityMap={0:"High Priority",1:"Medium Priority",2:"Low Priority",3:""}
#pages routes below

def pagesRouter(app,tasksDB):
    @app.route("/")
    def login():
        error = session.get("errorLogin",[[],[]])
        session["errorLogin"] = [[],[]]
        return render_template("login.html",signup=False,error = error)

    @app.route("/tasks")
    @jwt_required()
    def home():
        tokenData=get_jwt_identity()
        user = json.loads(tokenData)
        holder = list()
        currentCollection = tasksDB.tasks
        k=1
        err = session.get("errortask","")
        session["errortask"] = ""
        for i in currentCollection.find({"owner":user.get("email","")}):
            i['num'] = k
            k+=1
            i["priority"]=priorityMap[i["priority"]]
            holder.append(i)
        
        #shows newer tasks first
        holder.reverse() 
        #sorts accoring to priority
        holder.sort(key=lambda x: x.get('priority',3))
        
        return render_template("base.html",taskdata = holder,err=err)


    @app.route("/signup")
    def signup():
        error = session.get("errorLogin",[[],[]])
        session["errorLogin"] = [[],[]]
        return render_template("login.html",signup=True, error = error)
        
    @app.route("/update/<id>")
    @jwt_required()
    def update(id):
        currentCollection = tasksDB.tasks
        oid = ObjectId(id)
        err = session.get("errortask","")
        session["errortask"] = ""
        a = currentCollection.find({'_id':oid})[0]
        return render_template("Task.html", a = a,err=err)