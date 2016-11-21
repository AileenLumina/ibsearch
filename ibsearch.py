DOMAIN_REGULAR = 'https://ibsear.ch'
DOMAIN_NSFW = 'https://ibsearch.xxx'
IMAGES_PATH = '/api/v1/images.json'

class NoResults(Exception):
    pass

class UnexpectedResponseCode(Exception):
    pass

class IbSearch:
    def __init__(self, api_key, loop=None):
        self.api_key = api_key
        self.headers = {'X-IbSearch-Key': self.api_key}
        
        self.session = None
        
        if loop:
            self.loop = loop
    
    def _request(url, params={}, async_=False)
        if async_:
            import aiohttp
            if not self.session:
                self.session = aiohttp.ClientSession(loop = self.loop)
                with self.session as session:
                    with session.get(url, params=params, headers=self.headers) as res:
                        if not res.status == 200:
                            raise UnexpectedResponseCode(res.status)
                        result = self.loop.run_in_executor(res.json())
        else:
            import requests
            res = requests.get(url, headers=self.headers, params=params)
            if not res.status_code == 200:
                raise UnexpectedResponseCode(res.status)
            return res.json()
            
        return result
    
    def search(query, *, limit=None, page=1, nsfw_allowed=False,
               shuffle=False, shuffle_limit=None, async_=False):

        if nsfw_allowed:
            domain = DOMAIN_NSFW
        else:
            domain = DOMAIN_REGULAR
        
        # building querystring
        params = {}
        if limit:
            params['limit'] = limit
        if page is not 1:
            params['page'] = page
        if shuffle:
            params['shuffle'] = True
            if shuffle_limit:
                params['shuffle'] = shuffle_limit
            # Because this does not appear to work on IbSearch's end at the time of writing,
            # it needs to be done locally (see below).
        
        result = self._request(domain + IMAGES_PATH, querystring, async_)
        
        try:
            result[0]
        except IndexError:
            raise NoResults
        
        if shuffle:
            import random
            random.shuffle(result)
            if shuffle_limit:
                try:
                    result = result[0:shuffle_limit-1]
                except IndexError:
                    pass # Just return the shuffled list
        
        return result
    
    def get_random_image(query, nsfw_allowed=False):
        image_list = search(query, limit=100, nsfw_allowed=nsfw_allowed, shuffle=True, shuffle_limit=1)
