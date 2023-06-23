import inspect
import json
import logging
import uuid

from datetime import datetime


class Observability():

    def __init__(self):
        self.first_start_time = datetime.now()
        self.start_time = self.first_start_time
        self.end_time = self.first_start_time
        self.rid = uuid.uuid4()
        self.is_start_time_locked = False
        self.obj = {}

    def log(self, key, args=None):
        try:
            end_time = datetime.now()
            self.obj["action"] = key
            self.obj["context"] = inspect.stack()[1][1] + " " + str(inspect.stack()[1][2]) + " " + inspect.stack()[1][3]
            self.obj["rid"] = str(self.rid)
            self.obj["start"] = str(datetime.strptime(str(self.start_time), "%Y-%m-%d %H:%M:%S.%f"))
            self.obj["end"] = str(datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f"))
            self.obj["time_elapsed_sec"] = "{:.6f}".format((end_time - self.start_time).total_seconds())
            self.obj["total_time_elapsed_sec"] = "{:.6f}".format((end_time - self.first_start_time).total_seconds())
            self.obj["is_start_time_locked"] = self.is_start_time_locked
            if (args):
                self.obj["args"] = args
            logging.info(json.dumps(self.obj))
            if self.is_start_time_locked == False:
                # If start_time is NOT locked
                # - reset start_time to the last end_time (the current one),
                # If start_time IS locked
                # - pass here and it's going to use the end_time from the log before
                self.start_time = end_time
            self.obj = {}
        except:
            logging.error("An exception occurred parsing observability log.")

    def lock_time(self):
        self.is_start_time_locked = True

    def release_time(self):
        self.is_start_time_locked = False
        self.start_time = datetime.now()
