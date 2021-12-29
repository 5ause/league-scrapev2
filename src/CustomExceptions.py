class LoggableException(Exception):
    def __init__(self, msg="", thype=""):
        super().__init__(msg)
        if thype in ["alert", "warning", "msg"]:
            self.type = thype
        elif thype == "a":
            self.type = "alert"
        elif thype == "w":
            self.type = "warning"
        elif thype == "m":
            self.type = "msg"
        else:
            self.type = "msg"


class InstanceExistsException(LoggableException):
    pass


class APICallException(LoggableException):
    pass


class PlayerNotFoundException(LoggableException):
    pass


class InputException(LoggableException):
    pass


class SummonerException(LoggableException):
    def __init__(self, sum_name, msg="", thype=""):
        super().__init__(msg, thype)
        self.name = sum_name
