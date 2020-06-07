from collections import OrderedDict
from helpers import is_valid_latitude_and_longitude
from mergedeep import merge
from configs.api_formats import *


LATITUDE_CANDIDATE_KEYS = ['lat', 'Latitude']
LONGITUDE_CANDIDATE_KEYS = ['lng', 'Longitude']
NAME_CANDIDATE_KEYS = ['name', 'hotel_name', 'Name']
ADDRESS_CANDIDATE_KEYS = ['location', 'City', 'address', 'Country']
DESCRIPTION_CANDIDATE_KEYS = ['details', 'Description', 'info']
AMENITY_CANDIDATE_KEY = 'amenities'
IMAGE_CANDIDATE_KEY = 'images'
BOOKING_CONDITION_CANDIDATE_KEYS = ['booking_conditions']

ADDRESS_PICK_PRIORITY = ['address', 'location.address']
COUNTRY_PICK_PRIORITY = ['location.country', 'Country']
CITY_PICK_PRIORITY = ['City']


class HotelDetail:
    def __init__(self, hotel_id, destination_id, infos):
        self.infos = infos
        self.formulated_info = OrderedDict()
        self.formulated_info.update({
            ID_KEY: hotel_id,
            DESTINATION_KEY: destination_id
        })

    def formulate(self):
        self.formulate_name()
        self.formulate_location()
        self.formulate_description()
        self.formulate_images()
        self.formulate_booking_condition()
        self.formulate_amenities()
        return self.formulated_info

    def gather_piece_info(self, key):
        infos = []
        for source in self.infos:
            if key in source:
                infos.append(source[key])
        return infos

    @staticmethod
    def curate_amenities(amenities):
        curated = {}
        for item in amenities:
            if item and isinstance(item, dict):
                curated.update(item)
            elif item and isinstance(item, list):
                merge(curated, {'room': [amenity.lower() for amenity in item]})
        return curated

    @staticmethod
    def pick_from(obj, options):
        for option in options:
            try:
                if option.count('.') == 1:
                    layers = option.split('.')
                    layer1, layer2 = layers[0], layers[1]
                    return obj[layer1][layer2]
                else:
                    return obj[option]
            except KeyError:
                continue
        return ""

    @staticmethod
    def curate_images(images):
        result = {}
        image_set = set()
        for item in images:
            for key, value in item.items():
                current = []
                for image in value:
                    image_url = image['link'] if 'link' in image else image['url']
                    image_info = image['caption'] if 'caption' in image else image['description']
                    if image_url not in image_set:
                        current.append({
                            URL_KEY: image_url,
                            IMAGE_INFO_KEY: image_info
                        })
                        image_set.add(image_url)
                if key not in result:
                    result.update({key: current})
                else:
                    result[key] = result[key] + current
        return result

    def gather_candidate_infos(self, keys, one_only=False):
        candidates = {}
        for source in self.infos:
            for key in keys:
                if key in source:
                    if source[key] is not None:
                        if one_only:
                            return source[key]
                        candidates.update({key: source[key]})
        return candidates

    def formulate_name(self):
        name = self.gather_candidate_infos(NAME_CANDIDATE_KEYS, one_only=True)
        self.formulated_info.update({NAME_KEY: name})

    def formulate_location(self):
        location = {
            LATITUDE_KEY: None,
            LONGITUDE_KEY: None
        }

        latitude_candidates = self.gather_candidate_infos(LATITUDE_CANDIDATE_KEYS)
        longitude_candidates = self.gather_candidate_infos(LONGITUDE_CANDIDATE_KEYS)
        for i in range(len(LATITUDE_CANDIDATE_KEYS)):
            try:
                current_lat = latitude_candidates[LATITUDE_CANDIDATE_KEYS[i]]
                current_lng = longitude_candidates[LONGITUDE_CANDIDATE_KEYS[i]]
            except KeyError:
                continue
            if is_valid_latitude_and_longitude(current_lat, current_lng):
                location.update({
                    LATITUDE_KEY: current_lat,
                    LONGITUDE_KEY: current_lng
                })

        address_candidates = self.gather_candidate_infos(ADDRESS_CANDIDATE_KEYS)
        location.update({
            ADDRESS_KEY: self.pick_from(address_candidates, ADDRESS_PICK_PRIORITY),
            COUNTRY_KEY: self.pick_from(address_candidates, COUNTRY_PICK_PRIORITY),
            CITY_KEY: self.pick_from(address_candidates, CITY_PICK_PRIORITY)
        })

        self.formulated_info.update({LOCATION_KEY: location})

    def formulate_description(self):
        description_candidates = self.gather_candidate_infos(DESCRIPTION_CANDIDATE_KEYS)
        # Select the most descriptive one, that is the longest string.
        best_description = max(description_candidates.values(), key=len)
        self.formulated_info.update({DESCRIPTION_KEY: best_description})

    def formulate_amenities(self):
        amenity_pieces = self.gather_piece_info(AMENITY_CANDIDATE_KEY)
        curated_amenities = self.curate_amenities(amenity_pieces)
        self.formulated_info.update({AMENITY_KEY: curated_amenities})

    def formulate_images(self):
        images_pieces = self.gather_piece_info(IMAGE_CANDIDATE_KEY)
        curated_images = self.curate_images(images_pieces)
        self.formulated_info.update({IMAGE_KEY: curated_images})

    def formulate_booking_condition(self):
        condition = self.gather_candidate_infos(BOOKING_CONDITION_CANDIDATE_KEYS, one_only=True)
        self.formulated_info.update({BOOKING_CONDITION_KEY: condition})
