from MainObservation import GameObservation
import MainObservation
import RequestSender
import pickle
import json
import Logger
import main

# Logger.VERBOSITY_LEVEL = "VERBOSE"
RequestSender.add_keys(["RGAPI-6ec2c68c-5e1d-4ffa-821b-4af77abd8231", "RGAPI-36bd4d01-15b2-436d-b3e6-0e17b4f8c924"])


# print("TEAM 200")
# team_200 = players["200"]
# for player in team_200:
#     print(role)
#     print(team_100[role])

def save_game_object():
    obs = GameObservation('NA1_4144890019')
    file = open("sampleobs.bin", "wb")
    pickle.dump(obs, file)
    file.close()


def get_game_object():
    file = open("sampleobs.bin", "rb")
    obs = pickle.load(file)
    file.close()
    return obs


# Logger.VERBOSITY_LEVEL = "VERBOSE"
# obs = get_game_object()
# observation_dict = MainObservation.get_alllll_stats(obs)
# flattened_dict = main.flatten_obs_dict(observation_dict)
# print(json.dumps(flattened_dict, sort_keys=False, indent=4))

# observation1 = main.get_observation('NA1_4144890019')
# main.write_observation(observation1)
# print(json.dumps(observation1, sort_keys=False, indent=4))

print(main.get_seen())

# players = obs.players
# print(players)
# print("TEAM 100")
#
# team_100 = players["100"]
# for role in team_100:
#     # team_100[role] is a PlayerData object
#     print(role)
#     # MainObservation.check_ranked_stats(team_100[role])
#     # print(team_100[role].ranked_info)
#     print(MainObservation.get_game_stats(team_100[role]))
#
# print("TEAM 200")
