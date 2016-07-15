from datetime import datetime
import time
import pytz

from flask import current_app as app


#
# Time Helpers
#


def tz():
    import tzlocal
    return tzlocal.get_localzone()


def now():
    return datetime.now(tz=tz())


def fromtimestamp(timestamp):
    return datetime.fromtimestamp(timestamp).replace(tzinfo=tz())


def isostrptime(timestr):
    import re
    t = re.sub(r'[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))', '', timestr)
    return datetime.strptime(t, '%Y%m%dT%H%M%S.%f%z')


#
# Data Helpers
#

def id():
    from hashids import Hashids
    hid = Hashids(app.secret_key, 8)
    a, b = str(time.time()).split('.')
    return hid.encode(int(b))
