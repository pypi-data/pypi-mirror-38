import time
from datetime import timedelta

class Progress(object):

    poll_time = 1.0
    max_val = 0
    cur_val = 0
    start_time = 0
    last_update_time = 0
    next_update_time = 0

    def __init__(self, max_val, **kwargs):
        self.max_val = max_val
        self.poll_time = kwargs.get('poll_time', 1.0)

    def should_update(self):
        if time.time() >= self.next_update_time:
            return True
        return False

    def update(self, new_val):
        now = time.time()
        if self.start_time == 0:
            self.start_time = time.time()
        self.cur_val = new_val
        self.last_update_time = now
        self.next_update_time = now + self.poll_time

    @property
    def percentage(self):
        return (self.cur_val/self.max_val) * 100.

    @property
    def elapsed(self):
        return time.time() - self.start_time

    @property
    def remaining(self):
        left = 100. - self.percentage
        try:
            per_unit = self.elapsed/self.percentage
        except:
            per_unit = 1
        return left * per_unit

    def pretty_print(self):
        return "{:0.1f}% complete | {} elapsed | {} remaining".format(
            self.percentage,
            str(timedelta(seconds=int(self.elapsed))),
            str(timedelta(seconds=int(self.remaining)))
        )
