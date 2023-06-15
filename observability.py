import inspect
import logging
import uuid

from datetime import datetime


class Observability(logging.Logger):

    def __init__(self):
        self.first_start_time = datetime.now()
        self.start_time = self.first_start_time
        self.rid = uuid.uuid4()
        self.is_start_time_locked = False
        self.obj = {}

    def log(self, key, args=None):
        end_time = datetime.now()
        self.obj["action"] = key
        self.obj["context"] = inspect.stack()[1][1] + " " + str(inspect.stack()[1][2]) + " " + inspect.stack()[1][3]
        self.obj["rid"] = str(self.rid)
        self.obj["start"] = str(datetime.strptime(str(self.start_time), "%Y-%m-%d %H:%M:%S.%f"))
        self.obj["end"] = str(datetime.strptime(str(end_time), "%Y-%m-%d %H:%M:%S.%f"))
        self.obj["time_elapsed_sec"] = "{:.6f}".format((end_time - self.start_time).total_seconds())
        self.obj["total_time_elapsed_sec"] = "{:.6f}".format((end_time - self.first_start_time).total_seconds())
        if (args):
            self.obj["args"] = args
        print(self.obj)
        if self.is_start_time_locked == False:
            self.start_time = end_time
        self.obj = {}

    def lock_time(self):
        self.is_start_time_locked = True

    def release_time(self):
        self.is_start_time_locked = False
        self.start_time = datetime.now()
