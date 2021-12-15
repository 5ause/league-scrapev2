from src.CustomExceptions import InstanceExistsException


def get_api_key():
    if not APIKeyGetter.instance_exists:
        APIKeyGetter.single_instance = APIKeyGetter()
        APIKeyGetter.instance_exists = True
    return APIKeyGetter.single_instance


class APIKeyGetter:
    instance_exists = False
    single_instance = None

    def __init__(self):
        if APIKeyGetter.instance_exists:
            raise InstanceExistsException("Instance already exists")

    def get_key(self) -> str:
        # gets the API key to use
        # TODO consider making this a static method somewhere, and just have the requests use the method
        pass


class RequestQueue:

    def __init__(self):
        self.queue = []

    def enqueue(self) -> None:
        pass

    def process_and_dequeue(self) -> None:
        pass

    def is_empty(self) -> bool:
        return self.queue == []


# I THINK we can do a new request queue for each game, as we're gonna go game by game so it's fine. we'll process
# each request with the API key that it can use. I think we make an APIKEY object or something that will be a
# singleton and it'll track the last time a request was used then it takes the one used earliest, sleeps if
# necessary, then sends the requests.

class Request:
    def __init__(self, url: str) -> None:
        # observer should be type DataCollector.
        self.url = url
        self.results = None

    def process(self):
        # gets results by sending the request and getting the stuff
        # should throw an exception if you don't get 200.
        pass

    def get_results(self):
        if not self.has_results():
            # throw exception
            pass
        return self.results

    def has_results(self) -> bool:
        return self.results is not None
