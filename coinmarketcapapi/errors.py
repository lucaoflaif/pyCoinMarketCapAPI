"""Errors of pyCoinMarketCapAPI package"""

class APICallFailed(Exception):
    """This is raised whenever a server call doesn't return 200 http code"""
    def __init__(self, response):

        message = ("API Server didn't send a success (200) http code,"
                   "returned %(status_code)d instead from %(url)s") % {
                       'status_code': response.status_code,
                       'url': response.url
                       }

        super(APICallFailed, self).__init__(message)
