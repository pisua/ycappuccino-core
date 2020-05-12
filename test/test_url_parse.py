import unittest
from server import UrlPath

class testParseUrl(unittest.TestCase):

    def test_parse_service(self):
        w_call_service = UrlPath("http://test:1234/api/$service/monservice")
        self.assertEqual(w_call_service.get_service_name(), 'monservice')

    def test_parse_item_crud(self):
        w_call_service = UrlPath("http://test:1234/api/item")
        self.assertEqual(w_call_service.get_item_id(), 'item')

    def test_parse_service_param(self):
        w_call_service = UrlPath("http://test:1234/api/item?p1=v1&p2=v2")
        self.assertEqual(w_call_service.get_item_id(), 'item')
        self.assertEqual(w_call_service.get_params()["p1"], "v1")
        self.assertEqual(w_call_service.get_params()["p2"], "v2")


if __name__ == '__main__':
    unittest.main()
