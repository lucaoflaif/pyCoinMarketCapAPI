"""Errors of pyCoinMarketCapAPI package"""

class APIServerError(Exception):
    """This is raised whenever an error is retrieved from server"""
    def __init__(self, response):

        message = 'API Server returned "%(error)s" error message' % {'error': response['error']}

        super(APIServerError, self).__init__(message)

class APICallFailed(Exception):
    """This is raised whenever a server call doesn't return 200 http code"""
    def __init__(self, status_code):
  
        message = ("API Server didn't send a success (200) http code,",
                   "returned %(status_code)d instead") % {'status_code': status_code}

        super(APICallFailed, self).__init__(message)
