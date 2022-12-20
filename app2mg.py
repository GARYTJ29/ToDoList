#import mongodb in flask?
from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo


app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydb'

mongo = PyMongo(app)

# Routes
#from app import Foo  # noqa
@app.route("/")
def home():
    return "render_template(base.html, todo_list=todo_list)"

if __name__ == '__main__':
    app.run(debug=True)


from flask_restful import Resource


class Foo(Resource):
    def get(self, id):
        print(mongo)
        return {'get': 'Sample data'}

api.add_resource(Foo, '/foo', '/foo/<id>')


#from app import mongo  # noqa



