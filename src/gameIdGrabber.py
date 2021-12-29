import csv
from typing import List
from queue import Queue

import RequestSender
import APICollector

KEY = "RGAPI-6ec2c68c-5e1d-4ffa-821b-4af77abd8231"  # SINGLE KEY HERE
RequestSender.add_keys([KEY])  # KEY HERE

CSV_FILE = "../planning/games.csv"

START_ID = 'NA1_4144890019'  # START GAME ID HERE

FINAL_LIST = []
SEEN = [START_ID]
GAME_QUEUE = Queue()


def grab_participant_puuids(matchid):
    url = APICollector.MATCH_V5_URL
    variables = {"API_KEY": KEY, "MATCHID": matchid}
    game_json = RequestSender.send_request(url, variables=variables).json()
    return game_json["metadata"]["participants"]


def grab_participant_past_game(puuid) -> List[str]:
    variables = {"API_KEY": KEY, "PUUID": puuid, "COUNT": "10"}
    url = APICollector.PAST_MATCHES_URL
    return RequestSender.send_request(url, variables=variables).json()


def write_to_csv(games: List):
    with open(CSV_FILE, 'a', newline="") as file:
        writist = csv.writer(file, lineterminator="\n")
        for game in games:
            writist.writerow([game])


puuids = grab_participant_puuids(START_ID)
go = input("end to stop(" + str(len(FINAL_LIST)) + " games found)")
while go != "end":
    print("running...")
    for puuid in puuids:
        for game in grab_participant_past_game(puuid):
            # add all the new games it finds to the final list
            if game not in SEEN and game not in FINAL_LIST:
                FINAL_LIST.append(game)
            GAME_QUEUE.put(game)
    new_game_id = GAME_QUEUE.get()
    while new_game_id in SEEN:
        new_game_id = GAME_QUEUE.get()
    SEEN.append(new_game_id)
    puuids = grab_participant_puuids(new_game_id)
    go = input("end to stop(" + str(len(FINAL_LIST)) + " games found)")

write_to_csv(FINAL_LIST)
