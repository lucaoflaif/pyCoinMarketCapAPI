import os
import sys
import datetime
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import unittest

import coinmarketcapapi
from coinmarketcapapi import types
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

    def test_coin_public_method(self):
        coin_instance = self.my_class.coin(coin_name="ethereum")

        self.assertEqual(isinstance(coin_instance, types.Coin), True)
    def test_coins_public_method(self):
        for coin in self.my_class.coins():
            if not isinstance(coin, types.Coin):
                assert False, "Failed at %(coin)s" % {'coin': coin}


if __name__ == "__main__":
    unittest.main()
