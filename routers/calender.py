from flask import  render_template,  session
from flask_jwt_extended import (
 jwt_required, 
    get_jwt_identity, 
)
import json
from bson import ObjectId
# if u get cross origin error then use the below method before the router function
# @cross_origin()


#pages routes below

def CalpageRouter(app,tasksDB):
    @app.route("/calender")
    @jwt_required()
    def calender():
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
            holder.append(i)
        
        #shows newer tasks first
        holder.reverse() 
        #sorts accoring to priority
        holder.sort(key=lambda x: x.get('priority',3))
        
        return render_template("Calender.html",taskdata = holder,err=err)
