from typing import Dict
from queue import Queue
import traceback

import Logger
import csv
import json
import CustomExceptions
import RequestSender
import MainObservation
from MainObservation import GameObservation
import pandas as pd

CSV_FILE = "../planning/data.csv"
GAME_FILE = "../planning/games.csv"
BAD_SUMMONER_FILE = "../planning/bad_summoners.csv"
COLUMNS = ['gameid', 'winning_team', '100_TOP_avg_game_time', '100_TOP_positions_played', '100_TOP_avg_kda',
           '100_TOP_avg_kp', '100_TOP_avg_vision', '100_TOP_avg_cs', '100_TOP_goldpm', '100_TOP_dmgpm',
           '100_TOP_dmg_to_obj_pm', '100_TOP_wr', '100_TOP_tier', '100_TOP_rank', '100_TOP_lp', '100_TOP_wins',
           '100_TOP_losses', '100_TOP_veteran', '100_TOP_inactive', '100_TOP_freshblood', '100_TOP_hotstreak',
           '100_TOP_role_total_played', '100_TOP_role_wr', '100_TOP_champ_games_played', '100_TOP_champ_winrate',
           '100_JUNGLE_avg_game_time', '100_JUNGLE_positions_played', '100_JUNGLE_avg_kda', '100_JUNGLE_avg_kp',
           '100_JUNGLE_avg_vision', '100_JUNGLE_avg_cs', '100_JUNGLE_goldpm', '100_JUNGLE_dmgpm',
           '100_JUNGLE_dmg_to_obj_pm', '100_JUNGLE_wr', '100_JUNGLE_tier', '100_JUNGLE_rank', '100_JUNGLE_lp',
           '100_JUNGLE_wins', '100_JUNGLE_losses', '100_JUNGLE_veteran', '100_JUNGLE_inactive', '100_JUNGLE_freshblood',
           '100_JUNGLE_hotstreak', '100_JUNGLE_role_total_played', '100_JUNGLE_role_wr',
           '100_JUNGLE_champ_games_played', '100_JUNGLE_champ_winrate', '100_MIDDLE_avg_game_time',
           '100_MIDDLE_positions_played', '100_MIDDLE_avg_kda', '100_MIDDLE_avg_kp', '100_MIDDLE_avg_vision',
           '100_MIDDLE_avg_cs', '100_MIDDLE_goldpm', '100_MIDDLE_dmgpm', '100_MIDDLE_dmg_to_obj_pm', '100_MIDDLE_wr',
           '100_MIDDLE_tier', '100_MIDDLE_rank', '100_MIDDLE_lp', '100_MIDDLE_wins', '100_MIDDLE_losses',
           '100_MIDDLE_veteran', '100_MIDDLE_inactive', '100_MIDDLE_freshblood', '100_MIDDLE_hotstreak',
           '100_MIDDLE_role_total_played', '100_MIDDLE_role_wr', '100_MIDDLE_champ_games_played',
           '100_MIDDLE_champ_winrate', '100_BOTTOM_avg_game_time', '100_BOTTOM_positions_played', '100_BOTTOM_avg_kda',
           '100_BOTTOM_avg_kp', '100_BOTTOM_avg_vision', '100_BOTTOM_avg_cs', '100_BOTTOM_goldpm', '100_BOTTOM_dmgpm',
           '100_BOTTOM_dmg_to_obj_pm', '100_BOTTOM_wr', '100_BOTTOM_tier', '100_BOTTOM_rank', '100_BOTTOM_lp',
           '100_BOTTOM_wins', '100_BOTTOM_losses', '100_BOTTOM_veteran', '100_BOTTOM_inactive', '100_BOTTOM_freshblood',
           '100_BOTTOM_hotstreak', '100_BOTTOM_role_total_played', '100_BOTTOM_role_wr',
           '100_BOTTOM_champ_games_played', '100_BOTTOM_champ_winrate', '100_UTILITY_avg_game_time',
           '100_UTILITY_positions_played', '100_UTILITY_avg_kda', '100_UTILITY_avg_kp', '100_UTILITY_avg_vision',
           '100_UTILITY_avg_cs', '100_UTILITY_goldpm', '100_UTILITY_dmgpm', '100_UTILITY_dmg_to_obj_pm',
           '100_UTILITY_wr', '100_UTILITY_tier', '100_UTILITY_rank', '100_UTILITY_lp', '100_UTILITY_wins',
           '100_UTILITY_losses', '100_UTILITY_veteran', '100_UTILITY_inactive', '100_UTILITY_freshblood',
           '100_UTILITY_hotstreak', '100_UTILITY_role_total_played', '100_UTILITY_role_wr',
           '100_UTILITY_champ_games_played', '100_UTILITY_champ_winrate', '200_TOP_avg_game_time',
           '200_TOP_positions_played', '200_TOP_avg_kda', '200_TOP_avg_kp', '200_TOP_avg_vision', '200_TOP_avg_cs',
           '200_TOP_goldpm', '200_TOP_dmgpm', '200_TOP_dmg_to_obj_pm', '200_TOP_wr', '200_TOP_tier', '200_TOP_rank',
           '200_TOP_lp', '200_TOP_wins', '200_TOP_losses', '200_TOP_veteran', '200_TOP_inactive', '200_TOP_freshblood',
           '200_TOP_hotstreak', '200_TOP_role_total_played', '200_TOP_role_wr', '200_TOP_champ_games_played',
           '200_TOP_champ_winrate', '200_JUNGLE_avg_game_time', '200_JUNGLE_positions_played', '200_JUNGLE_avg_kda',
           '200_JUNGLE_avg_kp', '200_JUNGLE_avg_vision', '200_JUNGLE_avg_cs', '200_JUNGLE_goldpm', '200_JUNGLE_dmgpm',
           '200_JUNGLE_dmg_to_obj_pm', '200_JUNGLE_wr', '200_JUNGLE_tier', '200_JUNGLE_rank', '200_JUNGLE_lp',
           '200_JUNGLE_wins', '200_JUNGLE_losses', '200_JUNGLE_veteran', '200_JUNGLE_inactive', '200_JUNGLE_freshblood',
           '200_JUNGLE_hotstreak', '200_JUNGLE_role_total_played', '200_JUNGLE_role_wr',
           '200_JUNGLE_champ_games_played', '200_JUNGLE_champ_winrate', '200_MIDDLE_avg_game_time',
           '200_MIDDLE_positions_played', '200_MIDDLE_avg_kda', '200_MIDDLE_avg_kp', '200_MIDDLE_avg_vision',
           '200_MIDDLE_avg_cs', '200_MIDDLE_goldpm', '200_MIDDLE_dmgpm', '200_MIDDLE_dmg_to_obj_pm', '200_MIDDLE_wr',
           '200_MIDDLE_tier', '200_MIDDLE_rank', '200_MIDDLE_lp', '200_MIDDLE_wins', '200_MIDDLE_losses',
           '200_MIDDLE_veteran', '200_MIDDLE_inactive', '200_MIDDLE_freshblood', '200_MIDDLE_hotstreak',
           '200_MIDDLE_role_total_played', '200_MIDDLE_role_wr', '200_MIDDLE_champ_games_played',
           '200_MIDDLE_champ_winrate', '200_BOTTOM_avg_game_time', '200_BOTTOM_positions_played', '200_BOTTOM_avg_kda',
           '200_BOTTOM_avg_kp', '200_BOTTOM_avg_vision', '200_BOTTOM_avg_cs', '200_BOTTOM_goldpm', '200_BOTTOM_dmgpm',
           '200_BOTTOM_dmg_to_obj_pm', '200_BOTTOM_wr', '200_BOTTOM_tier', '200_BOTTOM_rank', '200_BOTTOM_lp',
           '200_BOTTOM_wins', '200_BOTTOM_losses', '200_BOTTOM_veteran', '200_BOTTOM_inactive', '200_BOTTOM_freshblood',
           '200_BOTTOM_hotstreak', '200_BOTTOM_role_total_played', '200_BOTTOM_role_wr',
           '200_BOTTOM_champ_games_played', '200_BOTTOM_champ_winrate', '200_UTILITY_avg_game_time',
           '200_UTILITY_positions_played', '200_UTILITY_avg_kda', '200_UTILITY_avg_kp', '200_UTILITY_avg_vision',
           '200_UTILITY_avg_cs', '200_UTILITY_goldpm', '200_UTILITY_dmgpm', '200_UTILITY_dmg_to_obj_pm',
           '200_UTILITY_wr', '200_UTILITY_tier', '200_UTILITY_rank', '200_UTILITY_lp', '200_UTILITY_wins',
           '200_UTILITY_losses', '200_UTILITY_veteran', '200_UTILITY_inactive', '200_UTILITY_freshblood',
           '200_UTILITY_hotstreak', '200_UTILITY_role_total_played', '200_UTILITY_role_wr',
           '200_UTILITY_champ_games_played', '200_UTILITY_champ_winrate']


def get_seen():
    df = pd.read_csv(CSV_FILE)
    return df['gameid'].tolist()


def get_bad_summoners():
    df = pd.read_csv(BAD_SUMMONER_FILE)
    return df['names'].tolist()


def add_bad_summoner(name):
    with open(BAD_SUMMONER_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writist = csv.writer(csvfile, lineterminator="\n")
        writist.writerow([name])


def get_games():
    df = pd.read_csv(GAME_FILE)
    game_queue = Queue()
    for gameid in df['gameid'].tolist():
        game_queue.put(gameid)
    return game_queue


# THE MAIN METHOD
# TODO learn sql and write to a database
def get_observation(matchid, bad_summoners=[]):
    obs = GameObservation(matchid, bad_players=bad_summoners)
    observation_dict = MainObservation.get_alllll_stats(obs)
    observation_dict["gameid"] = matchid
    flattened_dict = flatten_obs_dict(observation_dict)
    return flattened_dict


def write_observation(observation):
    with open(CSV_FILE, "a", newline="") as csvfile:
        writist = csv.DictWriter(csvfile, fieldnames=COLUMNS, lineterminator="\n")
        writist.writerow(observation)


def write_columns():
    with open(CSV_FILE, "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator="\n")
        writer.writerow(COLUMNS)


# was used ONCE to get columns
def get_columns():
    file = open("../planning/sample_flattened_data.json")
    data = json.load(file)
    return list(data.keys())


def flatten_obs_dict(obs_dict: Dict):
    ret_dict = dict()
    ret_dict["gameid"] = obs_dict.pop("gameid")
    ret_dict["winning_team"] = obs_dict.pop("winning_team")
    for team in obs_dict:
        for role in obs_dict[team]:
            role_dicts = obs_dict[team][role]
            # this should be where the game_stats, ranked_stats etc. are.
            for key in role_dicts:
                add_keys_with_offset(ret_dict, role_dicts[key], offset=team + "_" + role + "_")
            # so now tmp is populated with all the info for one role thing
    return ret_dict


def add_keys_with_offset(main_dict, other_dict, offset=""):
    for key in other_dict:
        if offset + key in main_dict:
            raise CustomExceptions.InputException("Some key already existed when trying to flatten dictionaries")
        main_dict[offset + key] = other_dict[key]


def main():
    API_KEYS = ["RGAPI-7394ad19-a9f9-45a2-ad8d-a3c87bdf666d", "RGAPI-b7e89e7a-8416-4795-a48f-40c911d8a7f5",
                "RGAPI-74c763e1-aaac-4dc1-9e82-86324ce0d8dc", "RGAPI-4eba76ba-5345-4418-9be7-4835b5033600"]
    Logger.VERBOSITY_LEVEL = "ALL"
    TARGET_OBS = int(input("target # of observations: "))

    RequestSender.add_keys(API_KEYS)

    SEEN = get_seen()
    bad_summoners = get_bad_summoners()

    # games to look at
    GAMES = get_games()  # queue
    Logger.message("Got game queue...")

    games_processed = 0
    errors = {"seen": 0, "bad_player": 0, "other": []}
    while games_processed < TARGET_OBS:
        gameid = GAMES.get()
        if gameid in SEEN:
            errors["seen"] += 1
            Logger.alert("already saw " + gameid)
            continue
        try:
            observation = get_observation(gameid, bad_summoners=bad_summoners)
            Logger.message("Got observation", gameid)
            write_observation(observation)
            Logger.message("Wrote observation", gameid)
            games_processed += 1
        except CustomExceptions.SummonerException as e:
            Logger.alert("bad summoner: " + e.name + " halted data collection for " + gameid)
            add_bad_summoner(e.name)
            bad_summoners.append(e.name)
            errors["bad_player"] += 1
        except TypeError as e:
            print(traceback.format_exc())
            Logger.alert("halted data collection for " + gameid + ". Message: " + str(e), str(type(e)))
        except Exception as e:
            Logger.alert("halted data collection for " + gameid + ". Message: " + str(e), str(type(e)))
            errors["other"].append(str(e))
        finally:
            SEEN.append(gameid)
            Logger.message("processed a total of " + str(games_processed) + " games.")
            Logger.message("error report: " + str(errors))
            # TODO check other functions to try to return good default values
            # TODO try to keep track of errors or something that occur...? and produce a report at the end.


if __name__ == "__main__":
    main()
