# -*- coding:utf-8 -*-

import sys

import enum


class ProgressBar(object):

    def __init__(self, max_num, unit_num=1):
        self.max_num = max_num
        self.unit_num = unit_num
        self.current_num = 0

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

    def update(self, num):
        self.current_num = max(0, min(self.max_num, num))

    def start(self):
        self.update(0)

    def finish(self):
        pass

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finish()


class CommandLineProgressBar(ProgressBar):

    LENGTH = 30
    BAR = '='
    TIP = '-'
    UNDER = '.'

    MessageType = enum.Enum(
        'MessageType',
        '''
        COURSE
        COMPLETE
        WARNING
        FAIL
        '''
    )

    def update(self, num):
        super(CommandLineProgressBar, self).update(num)
        if self.is_complete():
            self._write_complete()
            return
        self._write_course()

    def finish(self):
        super(CommandLineProgressBar, self).finish()
        if not self.is_complete():
            self._write_fail()
        self._line_brake()

    def _get_str(self):
        bar = int(self.LENGTH * self.progress)
        return '[{bar}{tip}{under}] {percentage}% ({current}/{max})'.format(
            bar=self.BAR * bar,
            tip=self.TIP if bar < self.LENGTH else self.BAR,
            under=self.UNDER * (self.LENGTH - bar),
            percentage=int(self.percentage),
            current=self.current_num,
            max=self.max_num)

    def _get_message_format(self, message_type=None):
        return {
            self.MessageType.COURSE.value: '\r\033[94m{message}\033[0m',
            self.MessageType.COMPLETE.value: '\r\033[92m{message}\033[0m',
            self.MessageType.WARNING.value: '\r\033[93m{message}\033[0m',
            self.MessageType.FAIL.value: '\r\033[91m{message}\033[0m',
        }.get(message_type) or '\r{message}'

    def _write(self, message, message_type=None):
        message_format = self._get_message_format(message_type)
        sys.stderr.write(message_format.format(message=message))
        sys.stderr.flush()

    def _write_course(self):
        self._write(self._get_str(), self.MessageType.COURSE.value)

    def _write_fail(self):
        self._write(self._get_str(), self.MessageType.FAIL.value)

    def _write_complete(self):
        self._write(self._get_str(), self.MessageType.COMPLETE.value)

    def _line_brake(self):
        self._write('\n')
