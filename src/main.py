from typing import Dict

import Logger
import CustomExceptions
import MainObservation
from MainObservation import GameObservation


def flatten_obs_dict(obs_dict: Dict):
    ret_dict = dict()
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
