from flask import  jsonify, request, redirect, url_for, make_response, session
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
     create_access_token, create_refresh_token,
    set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import json


def userRouter(app,usersDB):
    
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

    
    @app.route('/logout')
    def logout():
        resp = redirect(url_for("login"))
        unset_jwt_cookies(resp)
        return resp
