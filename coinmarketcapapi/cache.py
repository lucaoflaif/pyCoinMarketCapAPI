"""Cache Mechanism"""

import datetime
import pytz


class Cache:
    """Cache class"""
    def __init__(self, max_request_per_minute):
        self._delay_seconds = 60.0 / max_request_per_minute

        self._cached_api_ticker_response = None
        self._cached_api_global_response = None

        self._time_cached_api_response = None

        #number of API returned cached data
        self._n_cache_hits = 0

    def _get_cached_api_ticker_response(self):
        return self._cached_api_ticker_response

    def _get_cached_api_global_response(self):
        return self._cached_api_global_response

    ### PUBLIC METHODS ###

    def get_response(self, r_type):
        if r_type == 'ticker':
            return self._get_cached_api_ticker_response()
        elif r_type == 'global':
            return self._get_cached_api_global_response()

    def get_n_cache_hits(self):
        return self._n_cache_hits

    def get_time_cached_api_response(self):
        return self._time_cached_api_response

    def cached_data_is_old(self):

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

    def cache_data(self, json_response):
        #UTC time must be converted later into local user's time
        utc_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self._time_cached_api_response = utc_time

        if isinstance(json_response, list):
            # multiple values, that's a 'ticker' response
            self._cached_api_ticker_response = json_response
        else:
            # 'dict' instance, single value, 'global' response
            self._cached_api_global_response = json_response

    def set_n_cache_hits(self, hits=0, increment_by=None):
        if increment_by:
            self._n_cache_hits += increment_by
        else:
            self._n_cache_hits = hits

    def get_unset_cache(self):
        """return : returns a tuple (num_of_not_None_caches, [list of unset caches endpoint])
        """
        caches = []
        if self._cached_api_global_response is None:
            caches.append('global')
        if self._cached_api_ticker_response is None:
            caches.append('ticker')
        return (len(caches), caches)
