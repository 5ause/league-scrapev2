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
        Logger.debug("sending GET to " + url)
    else:
        response = requests.post(url=url, headers=headers)
        Logger.debug("sending POST to " + url)
    return response


def process_url(url, variables):
    if "<API_KEY>" in url and "API_KEY" not in variables:
        url = url.replace("<API_KEY>", get_api_key())
    if "<API_KEY>" in url and "API_KEY" in variables:
        url = url.replace("<API_KEY>", get_api_key(variables["API_KEY"]))
    for key in variables:
        url = url.replace("<" + key + ">", variables[key])
    return url


def get_api_key(api_key=None) -> str:
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
        time.sleep(time_between_reqs - (time_now - recent))

    # change the api key's last usage time to current time
    DICT_OF_KEYS[api_key] = round(time.time(), 1)
    return api_key
