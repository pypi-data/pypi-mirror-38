import unittest
from lxml import etree as ET
from pakettikauppa.merchant import decode_pdf_content, PkMerchant
from pakettikauppa.reseller import PkReseller


class TestGeneral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._merchant = PkMerchant(1)
        cls._reseller = PkReseller(1)

    def tearDown(self):
        """
        This method is called after each test
        """
        pass

    def test_empty_api_key(self):
        with self.assertRaises(Exception):
            merchant = PkMerchant(0, None, 'test')

    def test_empty_api_key_reseller(self):
        with self.assertRaises(Exception):
            merchant = PkReseller(0, None, 'test')

    def test_empty_secret_key(self):
        with self.assertRaises(Exception):
            merchant = PkMerchant(0, 'test', None)

    def test_empty_secret_key_reseller(self):
        with self.assertRaises(Exception):
            merchant = PkReseller(0, 'test', None)

    def test_create_merchant_object_in_live(self):
        creation_ok = 1
        try:
            merchant = PkMerchant(0, 'test api', 'test secret')
        except Exception:
            creation_ok = 0

        self.assertIs(creation_ok, 1)

    def test_create_reseller_object_in_live(self):
        creation_ok = 1
        try:
            merchant = PkReseller(0, 'test api', 'test secret')
        except Exception:
            creation_ok = 0

        self.assertIs(creation_ok, 1)

    def test_empty_pdf_content(self):
        with self.assertRaises(ValueError):
            decoded_pdf_content_string = decode_pdf_content('')

    def test_invalid_api_name_call(self):
        with self.assertRaises(Exception):
            h_config = self._merchant.get_api_config('list_customer')

    def test_invalid_api_name_call_reseller(self):
        with self.assertRaises(Exception):
            h_config = self._reseller.get_api_config('invalid_api_name')

    def test_get_api_conf(self):
        h_config = self._merchant.get_api_config('get_shipping_method_list')
        self.assertIsNotNone(h_config)

    def test_empty_input_create_consignment_element(self):
        with self.assertRaises(Exception):
            self._merchant._create_shipment_consignment_element('test', **{})

    def test_empty_consignment_parcel(self):
        root = ET.Element('ROOT')
        res = self._merchant._create_shipment_consignment_element(root, **{
            'Consignment.Reference': '3211479032410',
            'Consignment.Product': '90010',
            'Consignment.Currency': 'EUR',
            'Consignment.Invoicenumber': 'INV001',
            'Consignment.AdditionalInfo': {
                'AdditionalInfo.Text': 'Additional info text'
            },
            'Consignment.Contentcode': 'D',
            'Consignment.ReturnInstruction': None,
            'Consignment.Merchandisevalue': None,
            'Consignment.AdditionalService': None,
            'Consignment.Parcel': []
        })
        self.assertIsNone(res)

    def test_invalid_consignment_parcel(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_shipment_consignment_element(root, **{
                'Consignment.Reference': '3211479032410',
                'Consignment.Product': '90010',
                'Consignment.Currency': 'EUR',
                'Consignment.Invoicenumber': 'INV001',
                'Consignment.AdditionalInfo': {
                    'AdditionalInfo.Text': 'Additional info text'
                },
                'Consignment.Contentcode': 'D',
                'Consignment.ReturnInstruction': None,
                'Consignment.Merchandisevalue': None,
                'Consignment.AdditionalService': None,
                'Consignment.Parcel': 'test'
            })

    def test_invalid_content_code(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_shipment_consignment_element(root, **{
                'Consignment.Reference': '3211479032410',
                'Consignment.Product': '90010',
                'Consignment.Currency': 'EUR',
                'Consignment.Invoicenumber': 'INV001',
                'Consignment.AdditionalInfo': {
                    'AdditionalInfo.Text': 'Additional info text'
                },
                'Consignment.Contentcode': 'A',
                'Consignment.ReturnInstruction': None,
                'Consignment.Merchandisevalue': None,
                'Consignment.AdditionalService': None,
                'Consignment.Parcel': []
            })

    def test_invalid_return_instruction(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_shipment_consignment_element(root, **{
                'Consignment.Reference': '3211479032410',
                'Consignment.Product': '90010',
                'Consignment.Currency': 'EUR',
                'Consignment.Invoicenumber': 'INV001',
                'Consignment.AdditionalInfo': {
                    'AdditionalInfo.Text': 'Additional info text'
                },
                'Consignment.Contentcode': 'D',
                'Consignment.ReturnInstruction': 'A',
                'Consignment.Merchandisevalue': None,
                'Consignment.AdditionalService': None,
                'Consignment.Parcel': []
            })

    def test_empty_create_parcel_services_element(self):
        root = ET.Element('ROOT')
        res = self._merchant._create_parcel_service_elements(root, None)
        self.assertIsNone(res)

    def test_create_parcel_services_element(self):
        root = ET.Element('ROOT')
        error_found = 0
        try:
            self._merchant._create_parcel_service_elements(root, [{
                'test_key': 'test_value'
            }])
        except Exception:
            error_found = 1
        self.assertIs(error_found, 0)

    def test_empty_input_create_print_label_element(self):
        root = ET.Element('ROOT')
        with self.assertRaises(KeyError):
            self._merchant._create_print_label_element(root, **{})

    def test_empty_response_format_value_create_print_label_element(self):
        root = ET.Element('ROOT')
        with self.assertRaises(ValueError):
            self._merchant._create_print_label_element(root, **{
                'responseFormat': ''
            })

    def test_create_child_print_label_element(self):
        root = ET.Element('ROOT')
        error_found = 0
        try:
            self._merchant._create_child_print_label_element(root, **{
                'Code': 'test',
            })
        except Exception:
            error_found = 1

        self.assertIsNot(error_found, 1)

    def test_generate_multiple_tracking_codes_req(self):
        root = ET.Element('ROOT')
        error_found = 0
        try:
            self._merchant._create_child_print_label_element(root, **{
                'TrackingCode': [
                    {
                        'Code': 'JJFITESTLABEL601'
                    },
                    {
                        'Code': 'JJFITESTLABEL602'
                    },
                ]
            })
        except Exception:
            error_found = 1

        self.assertIsNot(error_found, 1)

    def test_invalid_key_create_child_print_label_element(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_child_print_label_element(root, **{
                'Code': {'InvalidKey': 'test'},
            })

    def test_validate_package_type(self):
        with self.assertRaises(Exception):
            self._merchant._validate_package_type('AB')

    def test_invalid_key_create_parcel_elements(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_parcel_elements(root, **{
                'Parcel.InvalidKey': 'test'
            })

    def test_empty_weight_unit(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_parcel_elements(root, **{
                'Parcel.Weight': {'weight_unit': '', 'value': '1.2'},
            })

    def test_empty_weight_unit_value(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_parcel_elements(root, **{
                'Parcel.Weight': {'weight_unit': 'kg', 'value': ''},
            })

    def test_default_volume_unit(self):
        root = ET.Element('ROOT')
        error_found = 0
        try:
            self._merchant._create_parcel_elements(root, **{
                'Parcel.Volume': {'unit': '', 'value': '0.6'},
            })
        except Exception:
            error_found = 1

        self.assertFalse(error_found)

    def test_empty_volume_unit_value(self):
        root = ET.Element('ROOT')
        with self.assertRaises(Exception):
            self._merchant._create_parcel_elements(root, **{
                'Parcel.Volume': {'unit': 'm3', 'value': ''},
            })

    def test_get_proper_req_data_create_shipment(self):
        with self.assertRaises(KeyError):
            req_data = self._merchant.get_proper_req_data_create_shipment(**{})

    def test_create_shipment_with_simple_data(self):
        simple_dict_data = self._merchant.get_simple_test_data_create_shipment()
        req_data = self._merchant.get_proper_req_data_create_shipment(**simple_dict_data)
        xml_req_data = self._merchant.get_xml_shipment_req_data(**req_data)

        self.assertIsNotNone(xml_req_data)


if __name__ == '__main__':
    unittest.main(verbosity=2)

