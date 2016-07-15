import re

from datetime import datetime
import pytz
from tzlocal import get_localzone


def dtz_now():
    return datetime.now(tz=get_localzone())


def dtz_from_time(timestamp):
    return datetime.fromtimestamp(
        timestamp
    ).replace(tzinfo=get_localzone())


def isostrptime(time_str):
    return datetime.strptime(
        re.sub(r'[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))', '', time_str),
        '%Y%m%dT%H%M%S.%f%z'
    )
