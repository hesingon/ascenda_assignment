import unittest
from configs.sources import *
from HotelController import *
from helpers import pretty_print_dict


class TestHotelController(unittest.TestCase):

    def test_merge_hotel_info(self):
        result = _merge_hotel_info('SjyX', DIRTY_HOTEL_DATA)
        pretty_print_dict(result)
        self.assertIsInstance(result, dict)

    def test_fetch_hotel_details(self):
        result = _fetch_hotel_details('iJhz')
        pretty_print_dict(result)
        self.assertIsInstance(result, dict)

    def test_get_hotel_from_db(self):
        result = query_one_hotel('iJhz')
        print(result)

    def test_save_hotel_to_db(self):
        result = _fetch_hotel_details('SjyX')
        pretty_print_dict(result)
        save_hotel_to_db(result)


if __name__ == '__main__':
    unittest.main()
