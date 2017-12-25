import os
import sys
import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import unittest

import coinmarketcapapi
from coinmarketcapapi import types, errors


class CacheTestCase(unittest.TestCase):
    """Test class
    """
    def test_error_from_server_is_raised(self):

        my_class = coinmarketcapapi.CoinMarketCapAPI()

        try:
            my_class.send_request(coin_name="bcoin")
            return False, "test not passed, error not raised"
        except Exception as e:
            return True, "Success! Error raised."


if __name__ == "__main__":
    unittest.main()
