from functools import partial
import requests


class AuthSession:
    def __init__(self, token):
        self.token = token

        # tasty hacky code
        for method in ['GET', 'POST', 'DELETE']:
            setattr(self, method.lower(), partial(self.authreq, method))

    def authreq(self, method, link, headers=None, json=None):
        method = method.lower()
        request_method = getattr(requests, method)

        if headers:
            headers['Authorization'] = self.token
        else:
            headers = {'Authorization': self.token}
        
        return request_method(link, headers=headers, json=json)
