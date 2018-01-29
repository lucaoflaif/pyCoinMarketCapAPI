"""Tests for the cache mechanism"""
import time
import secrets
import os
import sys
import unittest
import coinmarketcapapi

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))




class CacheTestCase(unittest.TestCase):
    """Test class
    """
    def test_class_can_cache_api_data_1(self):
        """This test will simulate an interation with the class making a request
        ina for loop, so the cache should be hit n times (where n is the number of
        for iterations) - 1 because the first one is always a call to the server
        (the cache is initially empty)
        """
        my_class = coinmarketcapapi.CoinMarketCapAPI(max_request_per_minute=9)
        times_of_request = 5

        for _ in range(times_of_request):
            my_class.send_request(convert="EUR")


        #self.assertEqual(my_class._n_cache_hits, times_of_request - 1)
        self.assertEqual(my_class.cache.get_n_cache_hits(), times_of_request - 1)

    def test_class_can_cache_api_data_2(self):
        """This test will simulate an interation with the class making a request
        every 3 seconds (under the cache time), so the cache should be hit 0 times
        """
        my_class = coinmarketcapapi.CoinMarketCapAPI(max_request_per_minute=30)
        times_of_request = 5

        for _ in range(times_of_request):
            my_class.send_request(convert="EUR")
            time.sleep(3)

         #self.assertEqual(my_class._n_cache_hits, 0)
        self.assertEqual(my_class.cache.get_n_cache_hits(), 0)

    def test_class_can_cache_api_data_3(self):
        """this test will simulate an interation with the class, the test will do some
        requests at different time and it'll see if the cache will hit the correct
        number of times
        """

        max_requests = 30
        my_class = coinmarketcapapi.CoinMarketCapAPI(max_request_per_minute=max_requests)

        delay_seconds = 60/max_requests
        n_of_requests = 5
        expected_cache_calls = 0
        total_cache_calls = 0

        for step in range(n_of_requests):
            my_class.send_request() # Server request
            #if my_class._n_cache_hits != 0:
            if my_class.cache.get_n_cache_hits() != 0:
                total_cache_calls += 1

            #random numbers generated securely
            delay_time = secrets.choice([1, 2, 3])

            time.sleep(delay_time)

            if (delay_time < delay_seconds) and step < 4: # less than last step, range is 0,1,2,3,4
                expected_cache_calls += 1

        self.assertEqual(total_cache_calls, expected_cache_calls)

    def test_force_full_cache(self):
        """This test will test the "force full test" mechanism
        """

        my_class = coinmarketcapapi.CoinMarketCapAPI(30, True)
        #max requests per minute 30
        #full cache mechanism True

        my_class.send_request(endpoint='ticker')

        time.sleep(3)
        my_class.send_request(endpoint='ticker')

        self.assertTrue(bool(my_class.cache._cached_api_global_response), True)



if __name__ == "__main__":
    unittest.main()
