import requests

import random
from json import json_decode


class NoResults(Exception):
    pass

class IbSearch:
    def __init__(self, api_key):
        self.API_KEY = api_key
    
    def search(query, *, limit=None, page=1, nsfw_allowed=False,
               shuffle=False, shuffle_limit=None):
        if nsfw_allowed:
            domain = 'ibsearch.xxx'
        else:
            domain = 'ibsear.ch'
        
        # building querystring
        querystring = "?q=" + query
        if limit:
            querystring.append('&limit=' + str(limit))
        if page is not 1:
            querystring.append('&page=' + str(page))
        if shuffle:
            querystring.append('&shuffle')
            if shuffle_limit:
                querystring.append('=' + str(shuffle_limit))
        # Because this does not appear to work on IbSearch's end at the time of writing,
        # it needs to be done locally (see below).
        
        result = json_decode(requests.get('https://' + domain + '/api/v1/images.json'
                                          + querystring, headers={'X-IbSearch-Key': self.API_KEY})
        
        if shuffle:
            random.shuffle(result)
            if shuffle_limit:
                result = result[0:shuffle_limit-1]
        
        return result
    
    def get_random_image(query, nsfw_allowed=False):
        return search(query, limit=100, nsfw_allowed=nsfw_allowed, shuffle=True, shuffle_limit=1)[0]
