from MainObservation import MainObservation
import RequestSender
import pickle
import Logger

# Logger.VERBOSITY_LEVEL = "VERBOSE"
RequestSender.add_keys(["RGAPI-6ec2c68c-5e1d-4ffa-821b-4af77abd8231", "RGAPI-36bd4d01-15b2-436d-b3e6-0e17b4f8c924"])

# obs = MainObservation('NA1_4144890019')
# file = open("sampleobs.bin", "wb")
# pickle.dump(obs, file)

file = open("sampleobs.bin", "rb")
obs = pickle.load(file)
file.close()

players = obs.players
print(players)
print("TEAM 100")

team_100 = players["100"]
for role in team_100:
    print(role)
    print(team_100[role])

print("TEAM 200")
team_200 = players["200"]
for player in team_200:
    print(role)
    print(team_100[role])
