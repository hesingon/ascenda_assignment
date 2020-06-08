from flask import Flask
from flask_restful import Api
from logic import Hotels
from configs.api_formats import API_URL_FIND_HOTELS

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

api.add_resource(Hotels, API_URL_FIND_HOTELS)

if __name__ == '__main__':
    app.run(debug=True)
