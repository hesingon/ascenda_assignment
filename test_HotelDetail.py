import unittest
from Models.HotelDetail import HotelDetail
from configs.sources import DIRTY_HOTEL_DATA
from helpers import pretty_print_dict


class TestHotelDetail(unittest.TestCase):

    def test_formuate(self):
        hotel = HotelDetail("iJhz", 5432, DIRTY_HOTEL_DATA)
        result = hotel.formulate()
        pretty_print_dict(result)

    def test_pick_from(self):
        test_input1 = {
            'location': {
                'address': '123 Omets Street, Jaffa, Jerusalem, Israel',
                'postal_code': '123123'
            }
        }
        result = HotelDetail.pick_from(test_input1, ['address', 'location.address'])
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
