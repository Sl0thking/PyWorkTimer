import json
from datetime import datetime, timedelta
import time


def get_timedelta_from_str(delta_str):
    t = datetime.strptime(delta_str.split(".")[0], "%H:%M:%S")
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

class WorkTimer:
    def __init__(self):
        self.work_timer = Timer()
        self.pause_timer = Timer()
        self.work_times = {}
        self.curr_date = None

    def track_day(self, date=None):
        if self.curr_date and self.curr_date == date:
            print("No new tracking")
            return

        if self.work_timer.duration() < timedelta(0):
            self.work_times[date]["work"] += self.work_timer.duration()

        if self.pause_timer.duration() < timedelta(0):
            self.work_times[date]["pause"] += self.pause_timer.duration()

        self.curr_date = date
        if self.curr_date not in self.work_times:
            self.work_times[date] = {
                "pause": timedelta(0),
                "work": timedelta(0)
            }

        self.work_timer.reset()
        self.pause_timer.reset()

    def start(self):
        self.work_timer.start()

    def stop(self):
        self.work_timer.stop()
        self.refresh()

    def pause(self):
        self.pause_timer.start()

    def unpause(self):
        self.pause_timer.stop()
        self.refresh()

    def refresh(self):
        self.work_times[self.curr_date]["work"] = self.work_timer.duration()
        self.work_times[self.curr_date]["pause"] = self.pause_timer.duration()

    def worktime(self, day):
        if day not in self.work_times:
            return timedelta(0)
        self.refresh()
        return self.work_times[day]["work"] - self.work_times[day]["pause"]

    def pausetime(self, day):
        if day not in self.work_times:
            return timedelta(0)
        self.refresh()
        return self.work_times[day]["pause"]

    def to_json(self):
        decoded_json = {}
        for date, times in self.work_times.items():
            decoded_json[date] = {
                "pause": str(times["pause"]),
                "work": str(times["work"]),
            }

        return json.dumps(decoded_json)

    def from_json(self, json_dict):
        self.work_times = json_dict
        self.work_timer.time = get_timedelta_from_str(json_dict[self.curr_date]["work"])
        self.pause_timer.time = get_timedelta_from_str(json_dict[self.curr_date]["pause"])
        self.refresh()

class Timer:

    def __init__(self):
        self.time = timedelta(0)
        self.start_time = None

    def reset(self):
        self.time = timedelta(0)
        self.start_time = None

    def start(self):
        if self.start_time:
            return

        self.start_time = datetime.now()

    def stop(self):
        if not self.start_time:
            return

        self.time += datetime.now() - self.start_time
        self.start_time = None

    def duration(self):
        acc_time = timedelta(0)
        if self.start_time:
            acc_time = datetime.now() - self.start_time

        acc_time += self.time

        return acc_time


if __name__ == "__main__":
    pause_timer = Timer()
    work_timer = Timer()
    work_timer.start()
    time.sleep(5)
    print(work_timer.duration())
    pause_timer.start()
    time.sleep(5)
    pause_timer.stop()
    work_timer.stop()
    print(work_timer.duration() - pause_timer.duration())