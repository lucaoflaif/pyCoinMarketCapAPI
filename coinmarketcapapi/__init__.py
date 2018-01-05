"""main file of package
"""

import json
import datetime
import requests
import pytz

from . import types, utils, errors
class CoinMarketCapAPI(object):
    '''API Class
    '''
    def __init__(self, max_request_per_minute=9):
        """: param int max_request_per_minute, if we want a maximum of {parameter}
             requests per minute, we don't have to make more than 1 request every
             ({parameter} / 60) seconds, IT'S FREAKIN' EASY M8
        """
        self._delay_seconds = 60.0 / max_request_per_minute

        self._cached_api_ticker_response = None
        self._cached_api_global_response = None

        self._time_cached_api_response = None

        #number of API returned cached data
        self._n_cache_hits = 0

    def __getattr__(self, attr):
        if attr == 'coins':
            return self._return_all_coins()
        elif attr == 'global_info':
            return self._return_global_info()
        return self._return_specific_coin(attr)

    def _return_all_coins(self):
        for coin in self._cached_api_ticker_response:
            yield types.Coin(*coin.values())

    def coins(self):
        """return a generator objects with the coin instance of all available coins.
        """
        return self._return_all_coins()

    def coin(self, coin_name):
        """return a coin instance of the {coin_name} coin.
        """
        return self._return_specific_coin(coin_name)

    def _return_specific_coin(self, attr):
        filtered_coins_dicts = utils.dicts_filter(self._cached_api_ticker_response, 'id', attr)
        selected_coin_values = filtered_coins_dicts[0].values()

        return types.Coin(*selected_coin_values)

    def global_info(self):
        """return a global instance with global market info
        """
        return self._return_global_info()

    def _return_global_info(self):
        global_info_values = self._cached_api_ticker_response.values()
        return types.Global(*global_info_values)

    _API_URL_ROOT = 'https://api.coinmarketcap.com/'
    _API_URL_VERSION = 'v1'


    def _make_url(self, endpoint, coin_name):
        url = "{}/{}/{}/{}".format(
            self._API_URL_ROOT,
            self._API_URL_VERSION,
            endpoint,
            coin_name or ""
        )
        return url

    def send_request(self, endpoint='ticker', coin_name=None, **kwargs):
        """: param string 'ticker', it's 'ticker' if we want info about coins,
            'global' for global market's info.
           : param string 'coin_name', specify the name of the coin, if None,
             we'll retrieve info about all available coins.
        """
        built_url = self._make_url(endpoint, coin_name)
        payload = dict(**kwargs)

        self._process_request(endpoint, built_url, payload)

    def get_response(self, data_type=None):
        """return json response from APIs converted into python list
           : param string 'data_type', if it's None it'll return the avaliable cache,
            if we've both global and ticker data, the function will return 'ticker' data,
            in that case, data_type should be assigned with 'ticker' or 'global'
        """
        if not data_type:
            return self._cached_api_ticker_response or self._cached_api_global_response
        elif data_type == 'ticker':
            return self._cached_api_ticker_response
        return self._cached_api_global_response

    def _cached_data_is_old(self):

        #If we haven't yet the time of last API call return True
        #in order to allow the code to do the request
        if not self._cached_api_ticker_response and not self._cached_api_global_response:
            return True

        #Let's check the time now
        time_now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

        #Then, calculate the difference between the last time
        # we retrieved new data from server and now
        time_difference = time_now_utc - self._time_cached_api_response

        seconds_difference = time_difference.total_seconds()

        if self._delay_seconds:
            return seconds_difference > self._delay_seconds

    def _process_request(self, endpoint, built_url, payload):

        #if we have no cache's time then call APIs, else use cached data
        if self._time_cached_api_response is None or self._cached_data_is_old():
            response = requests.get(built_url, params=payload)
            self._n_cache_hits = 0 # reset counter
        else:
            if endpoint == 'ticker':
                response = self._cached_api_ticker_response
            else:
                response = self._cached_api_global_response
            self._n_cache_hits += 1

        if self._response_is_valid(response):
            self._process_response(response)

    @classmethod
    def _response_is_valid(cls, response):
        if isinstance(response, (list, dict)): # jsonized response, already cached, no errors
            return True
        elif response.status_code != 200: # returned different status code from 200
            raise errors.APICallFailed(response)
        return True

    def _process_response(self, response):
        if isinstance(response, (list, dict)):
            #response already converted from json
            json_response = response
        else:
            #response in raw format, going to convert it
            json_response = response.json()

        self._cache_data(json_response)

    def _cache_data(self, json_response):
        #UTC time must be converted later into local user's time
        utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self._time_cached_api_response = utc_time

        if isinstance(json_response, list):
            # multiple values, that's a 'ticker' response
            self._cached_api_ticker_response = json_response
        else:
            # 'dict' instance, single vaue, 'global' response
            self._cached_api_global_response = json_response
