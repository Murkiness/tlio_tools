import requests


def get_avaiable_devices():
    r = requests.get("https://cbs.testdroid.com/api/v2/devices?filter=b_locked_eq_false&limit=50")
    return r.json()