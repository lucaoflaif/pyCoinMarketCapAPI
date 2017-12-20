import unittest
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


import time, random

import coinmarketcapapi

class CacheTestCase(unittest.TestCase):
    """Test class
    """
    def test_class_can_cache_api_data_1(self):
        
        my_class = coinmarketcapapi.CoinMarketCapAPI()
        times_of_request = 5

        for _ in range (times_of_request):
            my_class.send_request(convert="EUR")


        self.assertEqual(my_class._n_cache_hits, times_of_request - 1)

    def test_class_can_cache_api_data_2(self):

        my_class = coinmarketcapapi.CoinMarketCapAPI(max_request_per_minute=30)
        times_of_request = 5

        for _ in range(times_of_request):
            my_class.send_request(convert="EUR")
            time.sleep(3)

        self.assertEqual(my_class._n_cache_hits, 0)

    def test_class_can_cache_api_data_3(self):
        max_requests = 30
        my_class = coinmarketcapapi.CoinMarketCapAPI(max_request_per_minute=max_requests)

        delay_seconds = 60/max_requests
        n_of_requests = 5
        expected_cache_call = 0

        for step in range(n_of_requests):
            my_class.send_request() # Server request
            delay_time = random.uniform(1, 3)

            time.sleep(delay_time)

            if (delay_time < delay_seconds) and step < 4: # less than last step, range is 0,1,2,3,4
                expected_cache_call += 1

        self.assertEqual(my_class._n_cache_hits, expected_cache_call)


if __name__ == "__main__":
    unittest.main()