class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


VERBOSITY_LEVEL = "ALL"
VERBOSITY_DICT = {
    "VERBOSE": -1,
    "ALL": 0,
    "MSG": 1,
    "WARN": 2,
    "ALERT": 3,
    "NONE": 4
}


# ALL: all, MSG: msg, alert warning, WARN: alert warning, ALERT: alert, NONE: none

def check_if_send(level):
    return level >= VERBOSITY_DICT[VERBOSITY_LEVEL]


def verbose(msg: str, sender="debug") -> None:
    if not check_if_send(-1):
        return
    print("[" + sender + "]" + msg)


def debug(msg: str, sender="debug") -> None:
    if not check_if_send(0):
        return
    print("[" + sender + "] " + msg)


def alert(msg: str, sender="!!") -> None:
    if not check_if_send(3):
        return
    print(f"{BColors.FAIL}[" + sender + "] " + msg + f"{BColors.ENDC}")


def warning(msg: str, sender="!!") -> None:
    if not check_if_send(2):
        return
    print(f"{BColors.WARNING}[" + sender + "] " + msg + f"{BColors.ENDC}")


def message(msg: str, sender="  ") -> None:
    if not check_if_send(1):
        return
    print("[" + sender + "] " + msg)

# We don't need a complex logging system.
