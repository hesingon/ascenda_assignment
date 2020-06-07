from flask_restful import Resource
from flask import request, make_response
from ApiController import query_one_hotel, query_hotels
from configs.api_formats import API_HOTEL_ID_PARAM, \
    API_DESTINATION_ID_PARAM, API_PARAM_ERROR_MESSAGE


class Hotels(Resource):
    @staticmethod
    def get():
        args = request.args
        keys = list(args.keys())

        if API_HOTEL_ID_PARAM not in keys and \
                API_DESTINATION_ID_PARAM not in keys:
            return make_response(API_PARAM_ERROR_MESSAGE, 404)
        elif API_HOTEL_ID_PARAM in keys:
            result = query_one_hotel(args[API_HOTEL_ID_PARAM])
            return make_response(result, 200)
        elif API_DESTINATION_ID_PARAM in keys:
            result = query_hotels(args[API_DESTINATION_ID_PARAM])
            return make_response(result, 200)
