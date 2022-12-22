from flask import  request, redirect,  url_for, session
from flask.helpers import url_for
from flask_jwt_extended import (
  jwt_required, 
    get_jwt_identity,
)
import json
from bson import json_util
from bson import ObjectId


def taskRouter(app,tasksDB):
    
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
        taskdate = request.form.get("datetime")
        taskrepeat = request.form.getlist("repeat") 
        #print(request.form)
        if task == "":
            session["errortask"] = "Task Name can't be Blank"
            return redirect(url_for('home'))
        
        
        currentCollection.insert_one({'owner' : owner, "task":task , "date" : taskdate, "repeat" : taskrepeat})
        return redirect(url_for("home"))

    @app.route('/deleteTask/<id>')
    def deleteData(id):
        oid = ObjectId(id)
        currentCollection = tasksDB.tasks
        currentCollection.delete_one({'_id' : oid})
        return redirect(url_for('home'))

    @app.route('/updateTask/<id>', methods = ['POST'])
    def updateData(id):
        currentCollection = tasksDB.tasks
        oid = ObjectId(id)
        task = request.form.get("title")
        taskdate = request.form.get("datetime")
        taskrepeat = request.form.getlist("repeat") 
        if task == "":
            session["errortask"] = "Task Name can't be Blank"
            return redirect(f'/update/{id}')
        currentCollection.update_one({'_id':oid}, {"$set" : {'task' : task, "date" : taskdate, "repeat" : taskrepeat }})
        return redirect(url_for('home'))
