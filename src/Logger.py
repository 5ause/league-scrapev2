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


def alert(msg: str, sender="!!") -> None:
    print(f"{BColors.FAIL}[" + sender + "] " + msg + f"{BColors.ENDC}")


def warning(msg: str, sender="!!") -> None:
    print(f"{BColors.WARNING}[" + sender + "] " + msg + f"{BColors.ENDC}")


def message(msg: str, sender="  ") -> None:
    print("[" + sender + "] " + msg)

# We don't need a complex logging system.
