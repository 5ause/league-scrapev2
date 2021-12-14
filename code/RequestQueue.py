def get_request_queue():
    if not RequestQueue.instance_exists:
        RequestQueue.single_instance = RequestQueue()
        RequestQueue.instance_exists = True
    return RequestQueue.single_instance


class RequestQueue:
    instance_exists = False
    single_instance = None

    def __init__(self):
        if RequestQueue.instance_exists:
            raise TypeError("Instance already exists")
