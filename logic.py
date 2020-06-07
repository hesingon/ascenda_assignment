from flask_restful import Resource
from flask import request as this_req
import requests


class Hotels(Resource):
    def get(self):
        args = this_req.args
        supplier1 = requests.get('http://www.mocky.io/v2/5ebbea002e000054009f3ffc').json()
        supplier2 = requests.get('http://www.mocky.io/v2/5ebbea102e000029009f3fff').json()
        supplier3 = requests.get('http://www.mocky.io/v2/5ebbea1f2e00002b009f4000').json()
        res = supplier1 + supplier2 + supplier3
        # res.status_code = 200
        return res

