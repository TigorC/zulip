from __future__ import absolute_import

import datetime
import calendar
from django.utils.timezone import utc

def is_timezone_aware(datetime_object):
    # type: (datetime.datetime) -> bool
    return datetime_object.tzinfo is not None

def datetime_to_UTC(datetime_object):
    # type: (datetime.datetime) -> datetime.datetime
    if is_timezone_aware(datetime_object):
        return datetime_object.astimezone(utc)
    return datetime_object.replace(tzinfo=utc)

def floor_to_day(datetime_object):
    # type: (datetime.datetime) -> datetime.datetime
    return datetime.datetime(*datetime_object.timetuple()[:3]) \
                   .replace(tzinfo=datetime_object.tzinfo)

def timestamp_to_datetime(timestamp):
    # type: (float) -> datetime.datetime
    return datetime.datetime.utcfromtimestamp(float(timestamp)).replace(tzinfo=utc)

def datetime_to_timestamp(datetime_object):
    # type: (datetime.datetime) -> int
    return calendar.timegm(datetime_object.timetuple())

def datetime_to_string(datetime_object):
    # type: (datetime.datetime) -> str
    assert is_timezone_aware(datetime_object)
    date_string = datetime_object.strftime('%Y-%m-%d %H:%M:%S%z')
    return date_string
