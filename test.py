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

if __name__ == '__main__':
    test()
    loop.run_until_complete(async_test())
	nsfw_test()
