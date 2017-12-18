import os
import sys
import time
import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import unittest

import coinmarketcapapi

class CoinSelectMechanismTest(unittest.TestCase):
    

    my_class = coinmarketcapapi.CoinMarketCapAPI()

    my_class.send_request()
    response = my_class.get_response()

    coin_instance = my_class.bitcoin

    def test_class_attribute_returns_coin_instance(self):


        # To see if __getattr__ method returns correctly in instance of Coin class
        # we have to check if the value returned is an instance of that class.

        self.assertEqual(isinstance(self.coin_instance, coinmarketcapapi.types.Coin), True)

    def test_coin_intance_has_correct_values(self):


        coin_class_attributes = {attr: value for attr, value in self.coin_instance.__dict__.items()
                                 if not attr.startswith('__')}
        api_response_attributes = self.response[0]

        coin_class_attributes_values = coin_class_attributes.values()
        api_response_attributes_values = api_response_attributes.values()

        api_response_attributes = self.response[0]

        self.assertEqual(len(coin_class_attributes_values), len(api_response_attributes_values))



if __name__ == "__main__":
    unittest.main()
