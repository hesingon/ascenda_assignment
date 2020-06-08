from flask_restful import Resource
from flask import request, make_response
from HotelController import query_one_hotel, query_hotels, \
    update_db_new_hotel, should_update_all_hotels_for_destination, \
    update_db_hotels_by_desintation
from helpers import has_time_elapsed_for
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
            if not result or \
                    has_time_elapsed_for(result['updated_at'], 60):
                result = update_db_new_hotel(args[API_HOTEL_ID_PARAM])
            return make_response(result, 200)

        elif API_DESTINATION_ID_PARAM in keys:
            destination = int(args[API_DESTINATION_ID_PARAM])
            if should_update_all_hotels_for_destination(destination):
                print("Should update destination result")
                result = update_db_hotels_by_desintation(destination)
            else:
                result = query_hotels(destination)
            return make_response(result, 200)
