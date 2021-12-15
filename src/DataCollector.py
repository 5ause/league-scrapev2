from typing import List

from RequestQueue import Request


class DataCollector:
    request_list: List[Request]

    def __init__(self, gameid: str):
        self.request_list = []
        # todo consider making this a dict with tags so you know which request is which.

    def get_data(self):
        pass

    def process_data(self):
        # todo this should return a dictionary mapping observation name to the data value.
        # this will start putting shit inside the DataResult.
        # break into helper methods to process player, process game, etc.
        # probably do strategy pattern
        pass

    def check_requests_finished(self) -> bool:
        for r in self.request_list:
            if not r.has_results():
                return False
        return True


class DataResult:
    """
    This will hold the result of the data collection.
    """

    def __init__(self):
        # player info that could be obtained without shit
        # we'll probably save like blue_id1, blue_id2, then it points to other tables yeah...
        # TODO TODO TODO START HERE think of what we need to observe.
        self.players = {"blue": [None]*5,
                        "red": [None]*5}
        # match info on what happened in the match
        self.match_info = dict()
        self.match_info_blue_team = dict()
        self.match_info_red_team = dict()
