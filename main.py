from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,get_jwt_identity,get_jwt,create_access_token,set_access_cookies
)
from pymongo import MongoClient
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from datetime import datetime,timedelta,timezone

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

#refreshes the jwt token
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response

pagesRouter(app,tasksDB)
taskRouter(app,tasksDB)
userRouter(app,usersDB)


if __name__ == '__main__':
    app.run(debug = True)