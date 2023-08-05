import unittest
from pakettikauppa.reseller import PkReseller


class TestGetCustomer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._reseller = PkReseller(1)

    def test_get_config_data(self):
        h_config = self._reseller.get_api_config('list_customer')
        self.assertIsNotNone(h_config)

    def test_get_customer_list(self):
        list_data = self._reseller.get_customer_list()
        self.assertIsNotNone(list_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
