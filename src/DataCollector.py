import requests
import CustomExceptions


# TODO make a function that calls the riot api, returns a dict or an error
def get_rgapi_json(response: requests.Response):
    if response.status_code == 403:
        raise CustomExceptions.APICallException("No API KEY probably")
    elif not response.ok:
        raise CustomExceptions.APICallException("API Call failed, reason unknown.")
    else:
        return response.json()


# TODO remember that summoner_v4 by name has spaces as %20 instead of space btw

# TODO make a function that makes an object of name id puuid from the summoner v4 data

# TODO make a summoner_v4 object that processes the league_v4 stuff

class SampleClass:
    def __init__(self, summoner_name):
        json = self.send_request(summoner_name)
        self.process_json(json)

    def process_json(self, json):
        self.summoner_name = ""

    def send_request(self, summoner_name):
        pass
