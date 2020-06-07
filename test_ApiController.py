import unittest
from Sources import *
from ApiController import *
from helpers import pretty_print_dict


class TestApiController(unittest.TestCase):

    def test_retrieve_all_hotel_info(self):
        for id in HOTEL_ID:
            result = retrieve_all_hotel_info(id)
            pretty_print_dict(result)
            self.assertIsInstance(result, list)

    def test_merge_hotel_info(self):
        result = merge_hotel_info('SjyX', '5432', DIRTY_HOTEL_DATA)
        pretty_print_dict(result)
        self.assertIsInstance(result, dict)

    def test_fetch_hotel_details(self):
        result = fetch_hotel_details('SjyX', '5432')
        pretty_print_dict(result)
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
