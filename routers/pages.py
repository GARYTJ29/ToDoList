from flask import  render_template,  session
from flask_jwt_extended import (
 jwt_required, 
    get_jwt_identity, 
)
import json
from bson import ObjectId
from datetime import datetime
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
            i["prior"]=i.get("priority",3)
            i["priority"]=priorityMap[i.get("priority",3)]
            holder.append(i)
        
        #shows newer tasks first
        holder.reverse() 
        #sorts accoring to priority
        holder.sort(key=lambda x: x.get('prior',3))
        current_date = datetime.now().date()
        tasktdy = []
        
        for i in holder:
            if i.get("date") and datetime.strptime(i.get("date"), '%B %d, %Y %H:%M %p').date() >= current_date:
                if current_date.strftime("%A") in i.get("repeat",[]):
                    tasktdy.append(i)
                elif i.get("date","") != "":
                    date_object = datetime.strptime(i.get("date"), '%B %d, %Y %H:%M %p').date()
                    
                    if current_date == date_object:
                        tasktdy.append(i)
        #print(tasktdy)
        return render_template("base.html",taskdata = holder ,  tasktdy = tasktdy ,err=err)


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
        # a["priority"]=priorityMap[a.get("priority",3)]
        return render_template("Task.html", a = a,err=err)