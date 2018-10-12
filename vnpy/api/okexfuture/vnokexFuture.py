# encoding: UTF-8
import hashlib
import urllib


########################################################################
from vnpy.api.rest import RestClient, Request


########################################################################
class OkexFutureRestBase(RestClient):
    
    #----------------------------------------------------------------------
    def __init__(self):
        super(OkexFutureRestBase, self).__init__()
        self.apiKey = None
        self.apiSecret = None
    
    #----------------------------------------------------------------------
    # noinspection PyMethodOverriding
    def init(self, apiKey, apiSecret):
        # type: (str, str) -> any
        super(OkexFutureRestBase, self).init('https://www.okex.com/api/v1')
        self.apiKey = apiKey
        self.apiSecret = apiSecret

#----------------------------------------------------------------------
    def beforeRequest(self, req):  # type: (Request)->Request
        args = req.params or {}
        args.update(req.data or {})
        if 'sign' in args:
            args.pop('sign')
        if 'apiKey' not in args:
            args['api_key'] = self.apiKey
        data = urllib.urlencode(sorted(args.items()))
        data += "&secret_key=" + self.apiSecret
        
        sign = hashlib.md5(data.encode()).hexdigest().upper()
        data += "&sign=" + sign

        req.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        req.data = data
        return req

