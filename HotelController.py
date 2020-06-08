from flask import jsonify
import aiohttp
import asyncio
from configs.sources import SUPPLIERS_ENDPOINTS, \
    ID_IDENTIFIERS, DESTINTATION_IDENTIFIERS
from db_access import client as db
from Models.HotelDetail import HotelDetail
from helpers import time_now, has_time_elapsed_for


def _group_hotels_by_id(responses):
    hotels = {}
    for res in responses:
        for item in res:
            current_id = _get_id_from_json(item)
            if current_id not in hotels.keys():
                hotels.update({
                    current_id: []
                })
            hotels[current_id].append(item)
    return hotels


async def _fetch_hotels(session, url, destination):
    hotels = []
    async with session.get(url) as response:
        responses = await response.json()
        for res in responses:
            if _get_destination_from_json(res) == destination:
                hotels.append(res)
    return hotels


async def _fetch_from_suppliers_all_hotels(destination):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in SUPPLIERS_ENDPOINTS:
            tasks.append(_fetch_hotels(session, url, destination))
        htmls = await asyncio.gather(*tasks)
        return htmls


async def _fetch_specific_hotel(session, url, hotel_id):
    async with session.get(url) as response:
        responses = await response.json()
        for res in responses:
            if _get_id_from_json(res) == hotel_id:
                return res


async def _fetch_from_suppliers_single_hotel(hotel_id):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in SUPPLIERS_ENDPOINTS:
            tasks.append(_fetch_specific_hotel(session, url, hotel_id))
        htmls = await asyncio.gather(*tasks)
        return htmls


def _request_hotel(hotel_id=None, destination=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    result = None
    if hotel_id:
        result = loop.run_until_complete(
            _fetch_from_suppliers_single_hotel(hotel_id))
        # remove any None value from list
        result = list(filter(None.__ne__, result))
    elif destination:
        result = loop.run_until_complete(
            _fetch_from_suppliers_all_hotels(destination))
        result = _group_hotels_by_id(result)
    loop.close()
    return result


def _on_exception(request, exception):
    print("Problem: {}: {}".format(request.url, exception))


def _get_id_from_json(item):
    for key in ID_IDENTIFIERS:
        if key in item:
            return item[key]


def _get_destination_from_json(item):
    for key in DESTINTATION_IDENTIFIERS:
        if key in item:
            return item[key]


def _merge_hotel_info(data):
    hotel = HotelDetail(data)
    return hotel.formulate()


def update_db_new_hotel(hotel_id):
    data = _request_hotel(hotel_id=hotel_id)
    hotel_details = _merge_hotel_info(data)
    save_hotel_to_db(hotel_details)
    return hotel_details


def update_db_hotels_by_desintation(dest):
    data = _request_hotel(destination=dest)
    # hotel_details = _group_hotels_by_id(data)
    combined_details = []
    for _, hotel in data.items():
        detail = _merge_hotel_info(hotel)
        save_hotel_to_db(detail)
        combined_details.append(detail)
    db.ascenda.dest_update.update_one(
        {'dest': dest},
        {'$set': {'updated_at': time_now()}},
        upsert=True
    )
    return jsonify(combined_details)


def save_hotel_to_db(hotel_json):
    hotel_json.update({
        'updated_at': time_now()
    })
    db.ascenda.hotels.update_one(
        {'id': hotel_json['id']},
        {'$set': hotel_json},
        upsert=True
    )


def query_one_hotel(hotel_id):
    result = db.ascenda.hotels.find_one({'id': hotel_id})
    if result:
        del result['_id']
    return result


def query_hotels(destination_id):
    cursor = db.ascenda.hotels.find({'destination_id': destination_id})
    result = []
    for item in cursor:
        del item['_id']
        result.append(item)
    return jsonify(result)


def should_update_all_hotels_for_destination(dest):
    dest_info = db.ascenda.dest_update.find_one({'dest': dest})
    return not dest_info or has_time_elapsed_for(dest_info['updated_at'], 1)
