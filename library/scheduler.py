# turing-smart-screen-python - a Python system monitor and library for 3.5" USB-C displays like Turing Smart Screen or XuanFang
# https://github.com/mathoudebine/turing-smart-screen-python/

# Copyright (C) 2021-2023  Matthieu Houdebine (mathoudebine)
# Copyright (C) 2022-2023  Rollbacke
# Copyright (C) 2022-2023  Ebag333
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sched
import threading
import time
from datetime import timedelta
from functools import wraps

import library.config as config
import library.stats as stats
from library.log import logger

STOPPING = False


def async_job(threadname=None):
    """ wrapper to handle asynchronous threads """

    def decorator(func):
        """ Decorator to extend async_func """

        @wraps(func)
        def async_func(*args, **kwargs):
            """ create an asynchronous function to wrap around our thread """
            func_hl = threading.Thread(target=func, name=threadname, args=args, kwargs=kwargs)
            func_hl.start()
            return func_hl

        return async_func

    return decorator


def schedule(interval):
    """ wrapper to schedule asynchronous threads """

    def decorator(func):
        """ Decorator to extend periodic """

        def periodic(scheduler, periodic_interval, action, actionargs=()):
            """ Wrap the scheduler with our periodic interval """
            global STOPPING
            if not STOPPING:
                # If the program is not stopping: re-schedule the task for future execution
                scheduler.enter(periodic_interval, 1, periodic,
                                (scheduler, periodic_interval, action, actionargs))
            action(*actionargs)

        @wraps(func)
        def wrap(
                *args,
                **kwargs
        ):
            """ Wrapper to create our schedule and run it at the appropriate time """
            scheduler = sched.scheduler(time.time, time.sleep)
            periodic(scheduler, interval, func)
            scheduler.run()

        return wrap

    return decorator

@async_job("Track_Stats")
@schedule(timedelta(seconds=config.THEME_DATA['STATS']['TRACK'].get("INTERVAL", None)).total_seconds())
def TrackStats():
    #logger.debug("refresh track stats")
    stats.Track.names()
    stats.Track.progress()

@async_job("Device_Stats")
@schedule(timedelta(seconds=config.THEME_DATA['DIMAGE']['DEVICE'].get("INTERVAL", None)).total_seconds())
def DeviceStats():
    stats.Device.track_control()

@async_job("Coverart")
@schedule(timedelta(seconds=config.THEME_DATA['STATS']['DATE'].get("INTERVAL", None)).total_seconds())
def Coverart():
    stats.Cover.cover_art()

@async_job("Date_Stats")
@schedule(timedelta(seconds=config.THEME_DATA['STATS']['DATE'].get("INTERVAL", None)).total_seconds())
def DateStats():
    # logger.debug("Refresh date stats")
    stats.Date.stats()


@async_job("Queue_Handler")
@schedule(timedelta(milliseconds=1).total_seconds())
def QueueHandler():
    # Do next action waiting in the queue
    global STOPPING
    if STOPPING:
        # Empty the action queue to allow program to exit cleanly
        while not config.update_queue.empty():
            f, args = config.update_queue.get()
            f(*args)
    else:
        # Execute first action in the queue
        f, args = config.update_queue.get()
        if f:
            f(*args)


def is_queue_empty() -> bool:
    return config.update_queue.empty()
