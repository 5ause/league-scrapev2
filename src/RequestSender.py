from typing import List

import requests
import CustomExceptions
import time
import Logger

# dict will be key: time
DICT_OF_KEYS = dict()


def add_keys(keys: List[str]):
    for key in keys:
        DICT_OF_KEYS[key] = 0


# put API_KEY in variables if you need an api key.
def send_request(url: str, variables=dict(), headers=dict(), method="GET") -> requests.Response:
    # get api key or something
    url = process_url(url, variables)
    # send the req
    if method == "GET":
        response = requests.get(url=url, headers=headers)
        # Logger.verbose("sending GET to " + url)
    else:
        response = requests.post(url=url, headers=headers)
        # Logger.verbose("sending POST to " + url)
    return response


# eg. http://google.com/q=<VAR1>+<VAR2> where {"VAR1": "hello", "VAR2": "world"}
# http://google.com/q=hello+world
def process_url(url, variables):
    if "<API_KEY>" in url and "API_KEY" not in variables:
        key = get_api_key()
        url = url.replace("<API_KEY>", key)
        DICT_OF_KEYS[key] = round(time.time(), 1)
    if "<API_KEY>" in url and "API_KEY" in variables:
        key = get_api_key(variables["API_KEY"])
        url = url.replace("<API_KEY>", key)
        DICT_OF_KEYS[key] = round(time.time(), 1)
    for key in variables:
        url = url.replace("<" + key + ">", variables[key])
    return url


def get_api_key(api_key=None) -> str:
    # Logger.verbose("get_api_key_called")
    time_between_reqs = 1.2
    # int(time.time()) is in seconds ok
    # find the least recent key

    if api_key is None:
        recent = None
        for key in DICT_OF_KEYS:
            if recent is None or DICT_OF_KEYS[key] < recent:
                recent = DICT_OF_KEYS[key]
                api_key = key
        if recent is None or api_key is None:
            raise CustomExceptions.APICallException("No API keys entered.")
    else:
        recent = DICT_OF_KEYS[api_key]

    # Wait the appropriate amount of time
    time_now = round(time.time(), 1)
    if time_now - recent < time_between_reqs:
        Logger.verbose("about to sleep " + str(time_between_reqs - (time_now - recent)))
        time.sleep(time_between_reqs - (time_now - recent))

    # change the api key's last usage time to current time
    return api_key
