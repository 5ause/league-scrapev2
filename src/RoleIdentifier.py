from roleidentification import pull_data, get_roles
import CustomExceptions

DATA = pull_data()


def identify_roles(champions):
    # TOP JUNGLE MIDDLE BOTTOM UTILITY
    if len(champions) < 5:
        raise CustomExceptions.InputException("Did not get 5 champions for a team", "a")
    roles = get_roles(DATA, champions)
    return roles
