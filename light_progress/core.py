# -*- coding:utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from datetime import datetime


class Progress(object):

    def __init__(self, max_num, unit_num=1):
        self.max_num = max_num
        self.unit_num = unit_num
        self.current_num = 0
        self.started_at = None
        self.finished_at = None
        self.updated_at = None
        self.last_lap = 0
        self.average_lap = 0

    @classmethod
    def iteration(cls, iterable, call_back, **kwargs):
        with cls(len(iterable), **kwargs) as progress_bar:
            for item in iterable:
                call_back(item)
                progress_bar.forward()

    @classmethod
    def generation(cls, iterable, **kwargs):
        with cls(len(iterable), **kwargs) as progress_bar:
            for item in iterable:
                progress_bar.forward()
                yield item

    @property
    def progress(self):
        return float(self.current_num) / float(self.max_num)

    @property
    def percentage(self):
        return self.progress * 100

    @property
    def remaining(self):
        return self.max_num - self.current_num

    @property
    def elapsed_timedelta(self):
        return (self.finished_at or datetime.now()) - self.started_at

    @property
    def elapsed_seconds(self):
        return self.elapsed_timedelta.total_seconds()

    def is_complete(self):
        return self.max_num <= self.current_num

    def forward(self):
        self.update(self.current_num + self.unit_num)

    def back(self):
        self.update(self.current_num - self.unit_num)

    def _lap(self):
        now = datetime.now()
        current_lap = (now - (self.updated_at or now)).total_seconds()
        self.average_lap = ((self.last_lap or current_lap) + current_lap) / 2
        self.last_lap = current_lap
        self.updated_at = now

    def update(self, num):
        self._lap()
        self.current_num = max(0, min(self.max_num, num))

    def start(self):
        self.started_at = datetime.now()
        self.update(0)

    def finish(self):
        self.finished_at = datetime.now()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finish()
