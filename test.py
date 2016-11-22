import asyncio
import ibsearch

TEST_KEY = "my_key"
test_query = input("enter a test query: ")
loop = asyncio.get_event_loop()
cl = ibsearch.IbSearch(TEST_KEY, loop=loop)

def test():
    image1 = cl.get_random_image(test_query)
    print(image1.url)

@asyncio.coroutine
def async_test():
    image2 = yield from cl.get_random_image(test_query, async_=True)
    print(image2.url)
    
def nsfw_test():
    image3 = cl.get_random_image(test_query, nsfw_allowed=True)
    print(image3.url)
    
def multiple_test():
    images = cl.search(test_query, limit=5)
    for image in next(images):
        print(image.url)
        
def multiple_nsfw_test():
    images = cl.search(test_query, limit=5, nsfw_allowed=True)
    for image in next(images):
        print(image.url)
        
@asyncio.coroutine
def multiple_async_test():
    images = yield from cl.search(test_query, limit=5, async_=True)
    for image in images:
        print(image.url)

if __name__ == '__main__':
    test()
    loop.run_until_complete(async_test())
    nsfw_test()
    multiple_test()
    multiple_nsfw_test()
    loop.run_until_complete(multiple_async_test())