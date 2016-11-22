import asyncio
import ibsearch

TEST_KEY = "my_key"
test_query = input("enter a test query: ")
loop = asyncio.get_event_loop()
cl = ibsearch.IbSearch(TEST_KEY, loop=loop)


def test():
    image1 = cl.get_random_image(test_query)
    print(image1.url)


async def async_test():
    image2 = await cl.get_random_image(test_query, async_=True)
    image3 = await cl.async_get_random_image(test_query)
    print(image2.url)
    print(image3.url)
    
if __name__ == '__main__':
    test()
    loop.run_until_complete(async_test())