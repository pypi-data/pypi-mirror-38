# -*- coding: utf-8 -*-
#
#   Copyright (C) 2018 European Synchrotron Radiation Facility, Grenoble, France
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__authors__ = ["W. De Nolf"]
__license__ = "MIT"

import datetime
import dateutil.tz


def astimezone(dt, tz):
    try:
        return dt.astimezone(tz)
    except ValueError:
        return dt.replace(tzinfo=tz)


tzlocal = dateutil.tz.tzlocal()
tzutc = dateutil.tz.tzutc()
epoch = astimezone(datetime.datetime(1970, 1, 1), tzutc)


def totimestamp(dt):
    """
    :param datetime dt: assume local tz when tz-unaware
    :return int: seconds since UNIX epoch
    """
    return int(round((astimezone(dt, tzlocal) - epoch).total_seconds()))


def fromtimestamp(stamp, tz=tzlocal):
    """
    :param int stamp: seconds since UNIX epoch
    :param tzinfo tz: local by default (Optional)
    :return datetime: tz-aware
    """
    return datetime.datetime.fromtimestamp(stamp, tz)


def now(tz=tzlocal):
    """
    :param tzinfo tz: local by default
    :return datetime: tz-aware
    """
    return datetime.datetime.now(tz)


def add(dt, **kwargs):
    """
    :param datetime dt:
    :return datetime:
    """
    return dt + datetime.timedelta(**kwargs)
