def alert(msg: str, upper=True) -> None:
    if upper:
        msg = msg.upper()
    print("\n[!!]", msg, "\n")


def message(msg: str) -> None:
    print("[  ]", msg)
