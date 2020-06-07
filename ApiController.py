from flask import jsonify
from configs.Sources import SUPPLIERS_ENDPOINTS, ID_IDENTIFIER
from db_access import client as db
from Models.HotelDetail import HotelDetail
import aiohttp
import asyncio


async def fetch(session, url, hotel_id):
    async with session.get(url) as response:
        responses = await response.json()
        for res in responses:
            if get_id_from_json(res) == hotel_id:
                return res


async def main(hotel_id):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in SUPPLIERS_ENDPOINTS:
            tasks.append(fetch(session, url, hotel_id))
        htmls = await asyncio.gather(*tasks)
        return htmls


def async_request(hotel_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(hotel_id))
    loop.close()
    # remove any None value from list
    return list(filter(None.__ne__, result))


def on_exception(request, exception):
    print("Problem: {}: {}".format(request.url, exception))


def get_id_from_json(item):
    for key in ID_IDENTIFIER:
        if key in item:
            return item[key]


def merge_hotel_info(hotel_id, dest, data):
    hotel = HotelDetail(hotel_id, dest, data)
    return hotel.formulate()


def fetch_hotel_details(hotel_id, dest):
    data = async_request(hotel_id)
    hotel_merged_detail = merge_hotel_info(hotel_id, dest, data)
    return hotel_merged_detail


def save_hotel_to_db(hotel_json):
    result = db.ascenda.hotels.insert_one(hotel_json)


def query_one_hotel(hotel_id):
    result = db.ascenda.hotels.find_one({'id': hotel_id})
    del result['_id']
    return result


def query_hotels(destination_id):
    cursor = db.ascenda.hotels.find({'destination_id': destination_id})
    result = []
    for item in cursor:
        del item['_id']
        result.append(item)
    return jsonify(result)
