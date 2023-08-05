# -*- coding: utf-8 -*-
import logging
from time import time, sleep
from unittest import TestCase, main
from pakettikauppa.merchant import PkMerchant

try:
    import http.client as http_client
except ImportError:
    import httplib as http_client

# logging
http_client.HTTPConnection.debuglevel = 1
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
logging.basicConfig(
    level=logging.DEBUG,
)


class TestSearchPickupPoint(TestCase):
    @classmethod
    def setUpClass(cls):
        # Vilkas own key for customer id = 65 but end point must be in test mode
        cls.API_KEY = 'd4fb618f-1f44-4dc0-bdce-4993f4b91b77'
        cls.SECRET = 'b5c95243276d3ff398207f8dea3013fef001e6e5f51fb9cb2252f609608a81'

        cls._merchant = PkMerchant(1, cls.API_KEY, cls.SECRET)
        cls._test_merchant = PkMerchant(1)
        cls.logger = logging.getLogger(__name__)

    def tearDown(self):
        """
        This method is called after each test
        """
        pass

    def test_empty_parameter(self):
        with self.assertRaises(Exception) as e:
            self._merchant.search_pickup_points(**{})
        # self.logger.debug("Exception message = {}".format(e.exception))

    def test_empty_postal_code(self):
        with self.assertRaises(ValueError) as e:
            self._merchant.search_pickup_points(**{
                'postal_code': ''
            })
        # self.logger.debug("Exception message = {}".format(e.exception))
        self.assertEqual(str(e.exception), "Require postal code data")

    def test_search_pickup_points_with_postal_code_only(self):
        m = PkMerchant(1)
        list_data = m.search_pickup_points(**{
            'postal_code': '33100',
            'country_code2': '',
            'street_address': None,
            'service_provider': None,
            'max_result': None,
            'timestamp': None
        })
        self.assertIsNotNone(list_data)

    def test_search_pickup_points_with_street_address(self):
        input_params = {
            'postal_code': '33580',
            'country_code2': 'FI',
            'street_address': 'Nikinväylä 3 B 12',
            'service_provider': None,
            'max_result': None,
            'timestamp': str(int(time()))
        }
        list_data = self._merchant.search_pickup_points(**input_params)
        self.assertIsNotNone(list_data)

    def test_define_max_result(self):
        sleep(1)
        max_result_value = 5
        input_params = {
            'postal_code': '33210',
            'country_code2': '',
            'street_address': None,
            'service_provider': None,
            'max_result': max_result_value,
            'timestamp': str(int(time()))
        }
        list_data = self._merchant.search_pickup_points(**input_params)
        # print("list_data = {}".format(list_data))
        counter = 0
        if list_data is not None:
            for dict_item in list_data:
                counter = counter + 1

        self.logger.debug("Search result = {}".format(counter))
        self.assertLessEqual(counter, max_result_value) and not self.assertEqual(counter, 0)

    def test_search_db_schenker(self):
        sleep(1)
        list_data = self._merchant.search_pickup_points(**{
            'postal_code': '33200',
            'country_code2': 'FI',
            'street_address': None,
            'service_provider': 'DB Schenker',
            'max_result': 1,
            'timestamp': str(int(time()))
        })
        res_provider = ''
        if list_data is not None:
            for dict_item in list_data:
                res_provider = dict_item['provider']

        self.assertEqual(res_provider, 'DB Schenker')


if __name__ == '__main__':
    main(verbosity=2)
