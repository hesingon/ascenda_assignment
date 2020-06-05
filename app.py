from flask import Flask
from flask_restful import Api
from logic import Quotes, Hotels

app = Flask(__name__)
api = Api(app)

api.add_resource(Hotels, '/find_hotels')
api.add_resource(Quotes, '/')

if __name__ == '__main__':
    app.run(debug=True)
