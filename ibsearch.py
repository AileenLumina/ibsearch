DOMAIN_REGULAR = 'ibsear.ch/'
DOMAIN_NSFW = 'ibsearch.xxx/'
IMAGES_PATH = 'api/v1/images.json'

import random
import asyncio
import io

from urllib.parse import urlencode, unquote

class NoResults(Exception):
    pass

class UnexpectedResponseCode(Exception):
    pass

class Image:
    def __init__(self, loop, baseurl, **kwargs):
        self.format = kwargs.get("format")
        self.height = kwargs.get("height")
        self.width = kwargs.get("width")
        self.id = kwargs.get("id")
        self.path = kwargs.get("path")
        self.url = "http://" + kwargs.get("server") + "." + baseurl + self.path
        self.tags = kwargs.get("tags").split()
        self.loop = loop

    @asyncio.coroutine
    def _async_request(self):
        try:
            import aiohttp
        except ImportError:
            raise Exception("Aiohttp has to be installed to use this function.")
        else:

            with aiohttp.ClientSession(loop=self.loop) as session:
                res = yield from session.get(self.url)

                try:
                    if not res.status == 200:
                        raise UnexpectedResponseCode(res.status, (yield from res.text()))
                    result = yield from res.read()
                finally:
                    yield from res.release()

            return result

    def _request(self):
        try:
            import requests
        except ImportError:
            print("Requests has to be installed to use this function.")
        else:
            res = requests.get(self.url)
            if not res.status_code == 200:
                raise UnexpectedResponseCode(res.status_code, res.text)
            result = res.content
            return result
        
    def get_image_bytes(self, async_=False):
        """ Download the image and return the bytes """
        if async_:
            im_bytes = yield from self._async_request()
            bio = io.BytesIO()
            bio.write(im_bytes)
            bio.seek(0)
            return bio
        else:
            im_bytes = self._request()
            bio = io.BytesIO()
            bio.write(im_bytes)
            bio.seek(0)
            yield bio

    def save(self, async_=False, file=None):
        file = file or self.path.split("/")[-1]

        if async_:
            bio = yield from self.get_image_bytes()
        else:
            bio = next(self.get_image_bytes())

        with open(file, "wb") as f:
            f.write(bio.read())

        if async_:
            return file
        else:
            yield file

class IbSearch:
    def __init__(self, api_key, loop=None):
        self.api_key = api_key
        self.headers = {'X-IbSearch-Key': api_key}
        self.session = None
        if loop:
            self.loop = loop

    def build_url(self, url, params):
        """ Due to `params` as kwarg being % escaped """
        return url + "?" + unquote(urlencode(params))
    
    @asyncio.coroutine
    def _async_request(self, url, params=None):
        params = params or {}
        
        url = self.build_url(url, params)
        
        try:
            import aiohttp
        except ImportError:
            raise Exception("Aiohttp has to be installed to use this function.")
        else:
            with aiohttp.ClientSession(loop=self.loop) as session:
                res = yield from session.get(url, params=params, headers=self.headers)

                try:
                    if not res.status == 200:
                        raise UnexpectedResponseCode(res.status, (yield from res.text()))
                    result = yield from res.json()
                finally:
                    yield from res.release()

            return result

    def _request(self, url, params=None):
        params = params or {}

        url = self.build_url(url, params)
        
        try:
            import requests
        except ImportError:
            print("Requests has to be installed to use this function.")
        else:
            if not res.status_code == 200:
                raise UnexpectedResponseCode(res.status_code, res.text)
            result = res.json()
            return result

    @staticmethod
    def _build_params(query, limit, page, shuffle, shuffle_limit):
        params = {
            'q': query.replace(" ","+")
        }
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
        return params

    @asyncio.coroutine
    def async_search(self, *args):
        yield from self.search(*args, async_=True)

    def search(self, query, *, limit=None, page=1, nsfw_allowed=False,
               shuffle=False, shuffle_limit=None, async_=False):
        if nsfw_allowed:
            domain = DOMAIN_NSFW
        else:
            domain = DOMAIN_REGULAR

        params = self._build_params(query, limit, page, shuffle, shuffle_limit)

        url = "http://" + domain + IMAGES_PATH

        if async_:
            result = yield from self._async_request(url, params)
        else:
            result = self._request(url, params)

        if len(result) == 0:
            raise NoResults

        images = [Image(self.loop, domain, **d) for d in result]

        if shuffle:
            images = self.shuffle(images, shuffle_limit)

        if async_:
            return images
        else:
            yield images

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
        image_list = self.search(query, limit=100, nsfw_allowed=nsfw_allowed, shuffle=True, 
                                 shuffle_limit=1, async_=False)
        try:
            image = next(image_list)[0]
            return image
        except IndexError:
            # Not supposed to happen but here just in case
            raise NoResults

    @asyncio.coroutine
    def async_get_random_image(self, query, nsfw_allowed=False):
        image_list = yield from self.search(query, limit=100, nsfw_allowed=nsfw_allowed, 
                                                  shuffle=True, shuffle_limit=1, async_=True)
        try:
            image = image_list[0]
            return image
        except IndexError:
            # Not supposed to happen but here just in case
            raise NoResults
