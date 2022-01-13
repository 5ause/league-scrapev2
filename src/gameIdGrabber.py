import csv
from typing import List
from queue import Queue

import RequestSender
import APICollector
import pandas as pd

KEY = "RGAPI-00c7a9be-be3a-4833-9c65-0030abfde084"  # SINGLE KEY HERE
RequestSender.add_keys([KEY])  # KEY HERE

CSV_FILE = "../data/highelo/games.csv"
OTHER_SEEN_FILE = "../data/highelo/data.csv"

START_ID = 'NA1_4171314524'  # START GAME ID HERE

lst = [
    "NA1_4171314524",
    "NA1_4171262606",
    "NA1_4171210819",
    "NA1_4171132424",
    "NA1_4171024110",
    "NA1_4170855205",
    "NA1_4170777712",
    "NA1_4170658280",
    "NA1_4170654304",
    "NA1_4170494630",
    "NA1_4170449233",
    "NA1_4170480040",
    "NA1_4170370963",
    "NA1_4170322130",
    "NA1_4170245433",
    "NA1_4170192089",
    "NA1_4170162422",
    "NA1_4170112270",
    "NA1_4170032050",
    "NA1_4169953568"
]  # this is the current rank 1's last few games

FINAL_LIST = []
GAME_QUEUE = Queue()


def get_seen():
    df2 = pd.read_csv(OTHER_SEEN_FILE)
    return df2['gameid'].tolist()


def grab_participant_puuids(matchid):
    url = APICollector.MATCH_V5_URL
    variables = {"API_KEY": KEY, "MATCHID": matchid}
    game_json = RequestSender.send_request(url, variables=variables).json()
    return game_json["metadata"]["participants"]


def grab_participant_past_game(puuid) -> List[str]:
    variables = {"API_KEY": KEY, "PUUID": puuid, "COUNT": "5"}
    url = APICollector.PAST_MATCHES_URL
    return RequestSender.send_request(url, variables=variables).json()


def write_to_csv(games: List):
    with open(CSV_FILE, 'a', newline="") as file:
        writist = csv.writer(file, lineterminator="\n")
        for game in games:
            writist.writerow([game])


SEEN = [START_ID] + get_seen()
print("length of seen: " + str(len(SEEN)))

puuids = grab_participant_puuids(START_ID)
no_games = int(input("no. games: "))
while len(FINAL_LIST) < no_games:
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
    print("have " + str(len(FINAL_LIST)) + " games so far...")

FINAL_LIST = list(set(FINAL_LIST))
FINAL_FINAL_LIST = []
for gameid in FINAL_LIST:
    if gameid not in SEEN:
        FINAL_FINAL_LIST.append(gameid)

print("going to write " + str(len(FINAL_FINAL_LIST)) + " games")

write_to_csv(FINAL_FINAL_LIST)
