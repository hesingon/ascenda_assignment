from flask_restful import Resource
from flask import request, make_response
from HotelController import query_one_hotel, query_hotels, \
    update_db_new_hotel, should_update_all_hotels_for_destination, \
    update_db_hotels_by_destination
from helpers import has_time_elapsed_for
from configs.api_formats import API_HOTEL_ID_PARAM, \
    API_DESTINATION_ID_PARAM, ERROR_MESSAGE_API_PARAM, \
    DOCUMENT_KEY_UPDATE_AT, ERROR_MESSAGE_INVALID_PARAM, \
    ERROR_MESSAGE_NO_HOTEL_FOUND
from configs.settings import HOTEL_UPDATE_INTERVAL


class Hotels(Resource):
    @staticmethod
    def get():
        args = request.args
        keys = list(args.keys())

        if API_HOTEL_ID_PARAM not in keys and \
                API_DESTINATION_ID_PARAM not in keys:
            return make_response(ERROR_MESSAGE_API_PARAM, 404)

        elif API_HOTEL_ID_PARAM in keys:
            result = query_one_hotel(args[API_HOTEL_ID_PARAM])
            if not result or \
                    has_time_elapsed_for(result[DOCUMENT_KEY_UPDATE_AT],
                                         HOTEL_UPDATE_INTERVAL):
                try:
                    result = update_db_new_hotel(args[API_HOTEL_ID_PARAM])
                except Exception:
                    return make_response(ERROR_MESSAGE_NO_HOTEL_FOUND, 404)
            return make_response(result, 200)

        elif API_DESTINATION_ID_PARAM in keys:
            try:
                destination = int(args[API_DESTINATION_ID_PARAM])
            except ValueError:
                return make_response(ERROR_MESSAGE_INVALID_PARAM, 404)

            if should_update_all_hotels_for_destination(destination):
                print("Should update destination result")
                result = update_db_hotels_by_destination(destination)
            else:
                result = query_hotels(destination)

            return make_response(result, 200)
