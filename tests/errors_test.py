import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import unittest
import requests

import coinmarketcapapi
from coinmarketcapapi import errors


class CacheTestCase(unittest.TestCase):
    """Test class
    """

    my_class = coinmarketcapapi.CoinMarketCapAPI()

    def test_error_status_code_not_200(self):
        response = requests.get("http://www.google.com/invalidpage")

        with self.assertRaises(errors.APICallFailed):
            self.my_class._response_is_valid(response)

    def test_error_from_api_server(self):
        response = requests.get("https://api.coinmarketcap.com/v1/ticker/btcoin/")
        # URL should be ../bitcoin/

        with self.assertRaises(errors.APICallFailed):
            self.my_class._response_is_valid(response)

if __name__ == "__main__":
    unittest.main()
