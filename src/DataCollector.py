from typing import List

from RequestQueue import Request


class DataCollector:

    request_list: List[Request]

    def __init__(self, gameid: str):
        self.request_list = []
        # todo consider making this a dict with tags so you know which request is which.x

    def get_data(self):
        pass

    def process_data(self):
        # todo this should return a dictionary mapping observation name to the data value.
        # break into helper methods to process player, process game, etc.
        # probably do strategy pattern
        pass

    def check_requests_finished(self) -> bool:
        for r in self.request_list:
            if not r.has_results():
                return False
        return True
