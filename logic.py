from flask_restful import Resource
from flask import request, make_response
from ApiController import fetch_hotel_details, query_one_hotel, query_hotels


class Hotels(Resource):
    def get(self):
        args = request.args
        keys = list(args.keys())
        if 'hotel_id' not in keys and 'destination_id' not in keys:
            error_message = 'Please ensure either parameters hotel_id ' \
                            'or destination_id is passed'
            return make_response(error_message, 404)
        elif 'hotel_id' in keys:
            result = query_one_hotel(args['hotel_id'])
            return make_response(result, 200)
        elif 'destination_id' in keys:
            result = query_hotels(args['destination_id'])
            return make_response(result, 200)




