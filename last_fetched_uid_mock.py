last_fetched_uid = 960


def get_last_fetched_uid():
    return last_fetched_uid


def set_last_fetched_uid(value: int):
    global last_fetched_uid
    last_fetched_uid = value
