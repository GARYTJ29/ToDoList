from flask import  render_template,  session
from flask_jwt_extended import (
 jwt_required, 
    get_jwt_identity, 
)
import json
from datetime import datetime, timedelta
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
        current_date = datetime.now().date()
        seven_bef = current_date - timedelta(days = 30)
        seven_aff = current_date + timedelta(days = 30)
        weekday = {}
        j = seven_bef
        while ( j <= seven_aff):
            #print("task1")
            if j.strftime('%B %d, %Y %H:%M %p') not in weekday.get(j.strftime("%A"),[]):
                weekday[j.strftime("%A")] = weekday.get(j.strftime("%A"),[]) + [j.strftime('%B %d, %Y %H:%M %p')]
            j = j + timedelta(days = 1)
        weekTask = []
        for i in holder:
            last_date = seven_aff if i.get("date","") == "" else  datetime.strptime(i.get("date"), '%B %d, %Y %H:%M %p').date()
            for j in i.get("repeat",[]):
                for k in weekday.get(j,[]):
                    if datetime.strptime(k, '%B %d, %Y %H:%M %p').date() <= last_date:
                        m = i.copy()
                        m["date"] =  k
                        weekTask.append(m)
                        

        #print(weekday)

        return render_template("Calender.html",taskdata = holder , weekTask  = weekTask,err=err)
