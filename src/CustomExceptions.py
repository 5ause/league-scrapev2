class LoggableException(Exception):
    def __init__(self, type="", msg=""):
        super.__init__(msg)
        if type in ["alert", "warning", "msg"]:
            self.type = type
        elif type == "a":
            self.type = "alert"
        elif type == "w":
            self.type = "warning"
        elif type == "m":
            self.type = "msg"
        else:
            self.type = "msg"


class InstanceExistsException(LoggableException):
    pass


class APICallException(LoggableException):
    pass
