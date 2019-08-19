import os
from time import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from functools import wraps

from requests import get

URL = 'http://www.example.org'
CALL_COUNT = 200


def log_process_time(func):
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time()
        print('Starting %s ' % func.__name__)
        result = func(*args, **kargs)
        end = time()
        print('%s Took %.3f seconds to run' % (func.__name__, (end - start)))
        return result
    return wrapper


def http_call(index=None, url=URL):
    """
    :param index: str , defaults to random string 10 chars
    :param url:
    :return:
    """
    index = os.urandom(10) if index is None else index
    response = get(url)
    print('Response status %s for %s index count' %
          (response.status_code, index))
    return response.text


@log_process_time
def threads_io_run(call_count=CALL_COUNT):
    pool = ThreadPoolExecutor(max_workers=10)
    results = list(pool.map(http_call, range(call_count)))
    return results


@log_process_time
def process_io_run(call_count=CALL_COUNT):
    pool = ProcessPoolExecutor(max_workers=10)
    results = list(pool.map(http_call, range(call_count)))
    return results


async def run_futures_calls(loop, pool, call_count=CALL_COUNT):
    futures = [
        loop.run_in_executor(pool, http_call, index)
        for index in range(call_count)]
    await asyncio.wait(futures)


@log_process_time
def async_run(call_count=CALL_COUNT):
    loop = asyncio.get_event_loop()
    pool = ThreadPoolExecutor()
    loop.run_until_complete(run_futures_calls(loop, pool, call_count))


if __name__ == '__main__':
    # process_io_run()
    # threads_io_run()
    async_run()