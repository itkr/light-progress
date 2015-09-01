# -*- coding:utf-8 -*-

import sys

import enum


class ProgressBarBase(object):

    MessageType = enum.Enum(
        'MessageType',
        '''
        OK
        SUCCESS
        WARNING
        FAIL
        '''
    )

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
    def percent(self):
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
        message_type = self.MessageType.SUCCESS.value \
            if self.is_complete() else self.MessageType.OK.value
        self._echo(self.get_str(), message_type)

    def start(self):
        self.update(0)

    def finish(self):
        if not self.is_complete():
            self._echo(self.get_str(), self.MessageType.FAIL.value)
        self._echo('\n')

    def get_str(self):
        raise NotImplementedError

    def _get_message_format(self, message_type=None):
        raise NotImplementedError

    def _echo(self, message, message_type=None):
        message_format = self._get_message_format(message_type)
        sys.stderr.write(message_format.format(message=message))
        sys.stderr.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finish()


class StandardProgressBar(ProgressBarBase):

    LENGTH = 30
    BAR = '='
    TIP = '-'
    UNDER = '.'

    def _get_message_format(self, message_type=None):
        message_format = {
            self.MessageType.OK.value: '\r\033[94m{message}\033[0m',
            self.MessageType.SUCCESS.value: '\r\033[92m{message}\033[0m',
            self.MessageType.WARNING.value: '\r\033[93m{message}\033[0m',
            self.MessageType.FAIL.value: '\r\033[91m{message}\033[0m',
        }.get(message_type)
        return message_format or '\r{message}'

    def get_str(self):
        bar = int(self.LENGTH * self.progress)
        return '[{bar}{tip}{under}] {percent}% ({current}/{max})'.format(
            bar=self.BAR * bar,
            tip=self.TIP if bar < self.LENGTH else self.BAR,
            under=self.UNDER * (self.LENGTH - bar),
            percent=int(self.percent),
            current=self.current_num,
            max=self.max_num)


ProgressBar = StandardProgressBar
