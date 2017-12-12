import json
import requests
import datetime
import pytz

class CoinMarketCapAPI:
    '''API Class
    '''
    def __init__(self, max_request_per_minute = 9):
        """: param int max_request_per_minute, if we want a maximum of {parameter}
             requests per minute, we don't have to make more than 1 request every
             ({parameter} / 60) seconds, IT'S FREAKIN' EASY M8
        """
        self._delay_seconds = 60.0 / max_request_per_minute

        self._cached_api_response = None
        self._time_cached_api_response = None

        #number of API returned cached data
        self._n_cache_hits = 0

    API_URL_ROOT = 'https://api.coinmarketcap.com'
    API_URL_VERSION = 'v1'


    def _make_url(self, info_type):
        url = "{}/{}/{}".format(
            self.API_URL_ROOT,
            self.API_URL_VERSION,
            info_type
        )
        return url

    def send_request(self, info_type='ticker', **kwargs):
        """: param string 'ticker', it's 'ticker' if we want info about coins, 
            'global' for global market's info.
        """
        built_url = self._make_url(info_type)
        payload = dict(**kwargs)

        self._process_request(built_url, payload)
    
    def get_response(self):
        return self._cached_api_response

    def _cached_data_is_old(self):

        #If we haven't yet the time of last API call return True
        #in order to allow the code to do the request
        if not self._time_cached_api_response:
            return True

        #Let's check the time now
        time_now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
		
        #Then, calculate the difference between the last time 
        # we retrieved new data from server and now
        time_difference = time_now_utc - self._time_cached_api_response
        
        seconds_difference = time_difference.total_seconds()

        if self._delay_seconds:
            return seconds_difference > self._delay_seconds

    def _process_request(self, built_url, payload):

        #if we have no cache's time then call APIs, else use cached data
        if self._time_cached_api_response is None or self._cached_data_is_old():
            response = requests.get(built_url, params=payload)
        else:
            self._n_cache_hits += 1
            response = self._cached_api_response
        self._process_response(response)

    def _process_response(self, response):
        if isinstance(response, list):
            #response already converted from json
            self._cached_api_response = response
        else:
            #response in raw format, going to convert it
            self._cached_api_response = response.json()

        #UTC time must be converted later into local user's time
        utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self._time_cached_api_response = utc_time
