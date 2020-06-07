from flask import Flask
from flask_restful import Api
from flask_pymongo import PyMongo
from logic import Hotels

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo = PyMongo(app)
api = Api(app)

api.add_resource(Hotels, '/find_hotels')
# api.add_resource(Quotes, '/')

if __name__ == '__main__':
    app.run(debug=True)
