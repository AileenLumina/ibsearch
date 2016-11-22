DOMAIN_REGULAR = 'ibsear.ch/'
DOMAIN_NSFW = 'ibsearch.xxx/'
IMAGES_PATH = 'api/v1/images.json'

import random
import asyncio

class NoResults(Exception):
    pass

class UnexpectedResponseCode(Exception):
    pass

class Image:
    def __init__(self, baseurl, **kwargs):
        self.format = kwargs.get("format")
        self.height = kwargs.get("height")
        self.width = kwargs.get("width")
        self.id = kwargs.get("id")
        self.path = kwargs.get("path")
        self.url = "http://" + kwargs.get("server") + "." + baseurl + self.path
        self.tags = kwargs.get("tags").split()

class IbSearch:
    def __init__(self, api_key, loop=None):
        self.api_key = api_key
        self.headers = {'X-IbSearch-Key': self.api_key}
        self.session = None
        if loop:
            self.loop = loop

    @asyncio.coroutine
    def _async_request(self, url, params=None):
        params = params or {}
        try:
            import aiohttp
        except ImportError:
            raise Exception("Aiohttp has to be installed to use this function.")
        else:
            with aiohttp.ClientSession(loop=self.loop) as session:
                res = yield from session.get(url, params=params, headers=self.headers):
                if not res.status == 200:
                    raise UnexpectedResponseCode(res.status, yield from res.text())
                try:
                    result = yield from res.json()
                finally:
                    yield from res.release()
            return result

    def _request(self, url, params=None):
        params = params or {}
        try:
            import requests
        except ImportError:
            print("Requests has to be installed to use this function.")
        else:
            res = requests.get(url, headers=self.headers, params=params)
            if not res.status_code == 200:
                raise UnexpectedResponseCode(res.status, res.text)
            result = res.json()
            return result

    @asyncio.coroutine
    def async_search(self, query, *, limit=None, page=1, 
                           nsfw_allowed=False, shuffle=False, 
                           shuffle_limit=None):
        if nsfw_allowed:
            domain = DOMAIN_NSFW
        else:
            domain = DOMAIN_REGULAR
        # building querystring
        params = {}
        params['key'] = self.api_key
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
        result = yield from self._async_request("http://" + domain + IMAGES_PATH, params)
        try:
            result[0]
        except IndexError:
            raise NoResults
        images = [Image(domain, **d) for d in result]
        if shuffle:
            images = self.shuffle(images, shuffle_limit)
        return images
    
    def search(self, query, *, limit=None, page=1, nsfw_allowed=False,
               shuffle=False, shuffle_limit=None, async_=False):
        if async_:
            return self.async_search(query, limit=limit, page=page,
                                     nsfw_allowed=nsfw_allowed,
                                     shuffle=shuffle, 
                                     shuffle_limit=shuffle_limit)
        if nsfw_allowed:
            domain = DOMAIN_NSFW
        else:
            domain = DOMAIN_REGULAR
        # building querystring
        params = {}
        params['key'] = self.api_key
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
        result = self._request("http://" + domain + IMAGES_PATH, params)
        try:
            result[0]
        except IndexError:
            raise NoResults
        images = [Image(domain, **d) for d in result]
        if shuffle:
            images = self.shuffle(images, shuffle_limit)
        return images

    def shuffle(self, images, limit):
        random.shuffle(images)
        if limit:
            try:
                images = images[0:limit]
            except IndexError:
                pass # Just return the shuffled list
        return images

    def get_random_image(self, query, nsfw_allowed=False, async_=False):
        if async_:
            return self.async_get_random_image(query, nsfw_allowed=nsfw_allowed)
        image_list = self.search(query, limit=100, nsfw_allowed=nsfw_allowed, shuffle=True, shuffle_limit=1, async_=async_)
        try:
            image = image_list[0]
            return image
        except IndexError:
            # Not supposed to happen but here just in case
            raise NoResults

    @asyncio.coroutine
    def async_get_random_image(self, query, nsfw_allowed=False):
        image_list = yield from self.async_search(query, limit=100, nsfw_allowed=nsfw_allowed, shuffle=True, shuffle_limit=1)
        try:
            image = image_list[0]
            return image
        except IndexError:
            # Not supposed to happen but here just in case
            raise NoResults
