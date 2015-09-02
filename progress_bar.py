# -*- coding:utf-8 -*-

import sys
from datetime import datetime

import enum


class ProgressBar(object):

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
    def iteration(cls, iterable, call_back, unit_num=1):
        with cls(len(iterable), unit_num) as progress_bar:
            for item in iterable:
                call_back(item)
                progress_bar.forward()

    @property
    def progress(self):
        return float(self.current_num) / float(self.max_num)

    @property
    def percentage(self):
        return self.progress * 100

    @property
    def remaining(self):
        return self.max_num - self.current_num

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


class Widget(object):
    pass


class Bar(Widget):

    def __init__(self, length=30, bar='#', tip='>', under='.'):
        self.length = length
        self.bar = bar
        self.tip = tip
        self.under = under

    def get_str(self, context):
        bar_length = int(self.length * context.progress)
        return '[{bar}{tip}{under}]'.format(
            bar=self.bar * bar_length,
            tip=self.tip if bar_length < self.length else self.bar,
            under=self.under * (self.length - bar_length))


class Percentage(Widget):

    def get_str(self, context):
        return '{percentage}%'.format(percentage=int(context.percentage))


class Num(Widget):

    def get_str(self, context):
        return '({current}/{max})'.format(
            current=context.current_num, max=context.max_num)


class StartedAt(Widget):

    def get_str(self, context):
        return '{}'.format(context.started_at or '')


class FinishedAt(Widget):

    def get_str(self, context):
        return '{}'.format(context.finished_at or '')


class CommandLineProgressBar(ProgressBar):

    MessageType = enum.Enum(
        'MessageType',
        '''
        COMPLETE
        COURSE
        WARNING
        FAIL
        '''
    )

    def __init__(self, max_num, unit_num=1, widgets=[]):
        self.widgets = widgets or [Bar(), Percentage(), Num(),
                                   StartedAt(), '-', FinishedAt()]
        super(CommandLineProgressBar, self).__init__(max_num, unit_num)

    def update(self, num):
        super(CommandLineProgressBar, self).update(num)
        if not self.is_complete():
            self._write_course()

    def finish(self):
        super(CommandLineProgressBar, self).finish()
        self._write_complete() if self.is_complete() else self._write_fail()
        self._line_brake()

    def _get_str(self):
        return ' '.join([widget.get_str(self) if isinstance(widget, Widget)
                         else str(widget) for widget in self.widgets])

    def _get_message_format(self, message_type=None):
        return {
            self.MessageType.COMPLETE.value: '\r\033[92m{message}\033[0m',
            self.MessageType.COURSE.value: '\r\033[94m{message}\033[0m',
            self.MessageType.WARNING.value: '\r\033[93m{message}\033[0m',
            self.MessageType.FAIL.value: '\r\033[91m{message}\033[0m',
        }.get(message_type) or '\r{message}'

    def _write(self, message, message_type=None):
        message_format = self._get_message_format(message_type)
        sys.stderr.write(message_format.format(message=message))
        sys.stderr.flush()

    def _write_complete(self):
        self._write(self._get_str(), self.MessageType.COMPLETE.value)

    def _write_course(self):
        self._write(self._get_str(), self.MessageType.COURSE.value)

    def _write_warning(self):
        self._write(self._get_str(), self.MessageType.WARNING.value)

    def _write_fail(self):
        self._write(self._get_str(), self.MessageType.FAIL.value)

    def _line_brake(self):
        self._write('\n')
