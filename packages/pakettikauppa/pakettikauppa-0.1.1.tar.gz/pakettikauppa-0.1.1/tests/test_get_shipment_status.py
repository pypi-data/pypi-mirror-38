from unittest import TestCase, main
from pakettikauppa.merchant import PkMerchant


class TestGetShipmentStatus(TestCase):
    """
    Testing would require real tracking code
    """
    @classmethod
    def setUpClass(cls):
        cls._merchant = PkMerchant(1)
        cls.TRACKING_CODE = 'JJFI64574900000137203'

    def test_empty_tracking_code(self):
        with self.assertRaises(ValueError):
            self._merchant.get_shipment_status('')

    def test_get_shipment_status(self):
        res_obj = self._merchant.get_shipment_status(self.TRACKING_CODE)
        self.assertIsNotNone(res_obj)


if __name__ == '__main__':
    main(verbosity=2)
