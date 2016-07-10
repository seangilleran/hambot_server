import os
from datetime import datetime


class CamPhoto():

    def __init__(self, timestamp, path, *args, **kwargs):
        self.timestamp = timestamp
        self.path = path

    @staticmethod
    def get_all(path):
        rv = []
        for f in os.listdir(path):
            name, ext = os.path.splitext(f)
            if ext == ".jpg":
                rv.append(CamPhoto(
                    timestamp=datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(path, f))),
                    path=f
                ))
        return rv

    @staticmethod
    def get_latest(path):
        rv = None
        timestamp_prev = datetime.fromtimestamp(0)
        for f in os.listdir(path):
            name, ext = os.path.splitext(f)
            if ext == ".jpg":
                timestamp = datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(path, f)))
                if timestamp > timestamp_prev:
                    rv = CamPhoto(timestamp=timestamp, path=f)
                    timestamp_prev = timestamp
        return rv


class LogEntry():

    def __init__(self, timestamp, temperature, *args, **kwargs):
        self.timestamp = timestamp
        self.temperature = temperature

    @staticmethod
    def from_dict(data, time_str="%m/%d/%Y %H:%M:%S"):
        return LogEntry(
            timestamp=datetime.strptime(data["timestamp"], time_str),
            temperature=float(data["temp"])
        )

    @staticmethod
    def from_str(data, time_str="%m/%d/%Y %H:%M:%S"):
        time, temp = data.split("-")
        return LogEntry(
            timestamp=datetime.strptime(time, time_str),
            temperature=float(temp)
        )

    @staticmethod
    def add_new(path, log_entry, time_str="%m/%d/%Y %H:%M:%S"):
        rv = str(log_entry)
        with open(path, "a") as f:
            f.write(rv + os.linesep)
        LogEntry.trim_file(path)
        return rv

    @staticmethod
    def get_all(path, time_str="%m/%d/%Y %H:%M:%S"):
        rv = []
        with open(path) as f:
            lines = f.readlines()
        for line in lines:
            if "-" in line:
                rv.append(LogEntry.from_str(line))
        return rv

    @staticmethod
    def get_latest(path, count=24, time_str="%m/%d/%Y %H:%M:%S"):
        return LogEntry.get_all(path, time_str)[:count]

    @staticmethod
    def trim_file(path, max_lines=500):
        with open(path) as f:
            lines = f.readlines()
        while len(lines) > max_lines:
            lines.pop(0)
        with open(path, "w+") as f:
            f.writelines(lines)

    def __str__(self):
        return "{time}-{temp}".format(
            time=self.timestamp.strftime("%m/%d/%Y %H:%M:%S"),
            temp=str(self.temperature)
        )
