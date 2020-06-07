import unittest
from configs.Sources import *
from ApiController import *
from helpers import pretty_print_dict


class TestApiController(unittest.TestCase):

    def test_merge_hotel_info(self):
        result = merge_hotel_info('SjyX', '5432', DIRTY_HOTEL_DATA)
        pretty_print_dict(result)
        self.assertIsInstance(result, dict)

    def test_fetch_hotel_details(self):
        result = fetch_hotel_details('iJhz', '5432')
        pretty_print_dict(result)
        self.assertIsInstance(result, dict)

    def test_async_request(self):
        result = async_request()
        pretty_print_dict(result)

    def test_get_hotel_from_db(self):
        result = query_one_hotel('iJhz')
        print(result)

    def test_save_hotel_to_db(self):
        result = fetch_hotel_details('f8c9', '1122')
        pretty_print_dict(result)
        save_hotel_to_db(result)


if __name__ == '__main__':
    unittest.main()
