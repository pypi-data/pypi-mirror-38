"""
CARPI REDIS DATA BUS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""

from __future__ import print_function
from datetime import datetime
from pytz import utc
from tzlocal import get_localzone
from traceback import print_exception
import sys


TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f %Z%z'


def _get_utc_now():
    return datetime.now(utc).strftime(TIMESTAMP_FORMAT)


def _get_local_now():
    return datetime.now(get_localzone()).strftime(TIMESTAMP_FORMAT)


def log(msg):
    print("{} | {}".format(_get_utc_now(), msg))


def stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def err_log(msg):
    stderr("{} | {}".format(_get_utc_now(), msg))


def both_log(msg):
    m = "{} | {}".format(_get_utc_now(), msg)
    log(m)
    stderr(m)


def print_unhandled_exception():
    exc_type, exc, traceback = sys.exc_info()
    both_log("An unexpected error has occurred!")
    print_exception(exc_type, exc, traceback, limit=64)
    del exc_type, exc, traceback


if __name__ == '__main__':
    err_log("This script is not intended to be run standalone!")
