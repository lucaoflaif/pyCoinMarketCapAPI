"""main file of package
"""

import requests

from . import types, cache, utils, errors
class CoinMarketCapAPI(object):
    '''API Class
    '''
    def __init__(self, max_request_per_minute=9):
        """: param int max_request_per_minute, if we want a maximum of {parameter}
             requests per minute, we don't have to make more than 1 request every
             ({parameter} / 60) seconds, IT'S FREAKIN' EASY M8
        """
        self.cache = cache.Cache(max_request_per_minute)

    def __getattr__(self, attr):
        if attr == 'coins':
            return self._return_all_coins()
        elif attr == 'global_info':
            return self._return_global_info()
        return self._return_specific_coin(attr)

    def _return_all_coins(self):
        for coin in self.cache.get_response(r_type='ticker'):
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
        filtered_coins_dicts = utils.dicts_filter(self.cache.get_response(r_type='ticker'),
                                                  'id',
                                                  attr)
        selected_coin_values = filtered_coins_dicts[0].values()

        return types.Coin(*selected_coin_values)

    def global_info(self):
        """return a global instance with global market info
        """
        return self._return_global_info()

    def _return_global_info(self):
        global_info_values = self.cache.get_response(r_type='global').values()
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
            return self.cache.get_response(r_type='ticker') or self.cache.get_response(r_type='global')
        elif data_type == 'ticker':
            return self.cache.get_response(r_type='ticker')
        return self.cache.get_response(r_type='global')

    def _process_request(self, endpoint, built_url, payload):

        #if we have no cache's time then call APIs, else use cached data
        if self.cache.get_time_cached_api_response() is None or self.cache.cached_data_is_old():
            response = requests.get(built_url, params=payload)
            self.cache.set_n_cache_hits(0) # reset counter
        else:
            if endpoint == 'ticker':
                response = self.cache.get_response(r_type='ticker')
            else:
                response = self.cache.get_response(r_type='global')
            self.cache.set_n_cache_hits(increment_by=1)

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

        self.cache.cache_data(json_response)
