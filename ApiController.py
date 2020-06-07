import json
import grequests
from Sources import SUPPLIERS, ID_IDENTIFIER
from HotelDetail import HotelDetail


def on_exception(request, exception):
    print("Problem: {}: {}".format(request.url, exception))


def get_id_from_json(item):
    for key in ID_IDENTIFIER:
        if key in item:
            return item[key]


def retrieve_all_hotel_info(hotel_id):
    responses = grequests.map(
        (grequests.get(u) for u in SUPPLIERS),
        exception_handler=on_exception, size=5)
    hotel_info = []
    for res in responses:
        trimmed_res = json.loads(res.text)
        for item in trimmed_res:
            if get_id_from_json(item) == hotel_id:
                hotel_info.append(item)
                break
    return hotel_info


def merge_hotel_info(hotel_id, dest, data):
    hotel = HotelDetail(hotel_id, dest, data)
    return hotel.formulate()


def fetch_hotel_details(hotel_id, dest):
    data = retrieve_all_hotel_info(hotel_id)
    hotel_merged_detail = merge_hotel_info(hotel_id, dest, data)
    return hotel_merged_detail
