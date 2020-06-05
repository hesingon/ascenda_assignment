from flask_restful import Resource
from flask import request


class Hotels(Resource):
    def get(self):
        args = request.args

        return args


class Quotes(Resource):
    def get(self):
        return {
            'William Shakespeare': {
                'quote': ['Love all,trust a few,do wrong to none',
                          'Some are born great, some achieve greatness, and some greatness thrust upon them.']
            },
            'Linus': {
                'quote': ['Talk is cheap. Show me the code.']
            }
        }
