# -*- coding:utf-8 -*-

import sys

import enum

MessageType = enum.Enum(
    'MessageType',
    '''
    OK
    SUCCESS
    WARNING
    FAIL
    '''
)


class ProgressBar(object):

    LENGTH = 30
    BAR = '='
    TIP = '-'
    BASE = '.'

    def __init__(self, max_num, unit_num=1):
        self.max_num = max_num
        self.unit_num = unit_num
        self.current_num = 0

    @property
    def progress(self):
        return float(self.current_num) / float(self.max_num)

    def is_complete(self):
        return self.max_num <= self.current_num

    def forward(self):
        self.update(self.current_num + self.unit_num)

    def back(self):
        self.update(self.current_num - self.unit_num)

    def update(self, num):
        self.current_num = max(0, min(self.max_num, num))

        message_type = MessageType.SUCCESS.value \
            if self.is_complete() else MessageType.OK.value

        self._echo(self._get_str(), message_type)

    def start(self):
        self.update(0)

    def finish(self):
        if not self.is_complete():
            self._echo(self._get_str(), MessageType.FAIL.value)
        self._echo('\n')

    def _get_str(self):
        bar = int(self.LENGTH * self.progress)
        return '[{bar}{tip}{base}] {progress}% ({current}/{max})'.format(
            bar=(self.BAR * bar),
            tip=(self.TIP if bar < self.LENGTH else self.BAR),
            base=self.BASE * (self.LENGTH - bar),
            progress=int(self.progress * 100),
            current=self.current_num,
            max=self.max_num)

    def _echo(self, message, message_type=None):
        color = {
            MessageType.OK.value: '\033[94m',
            MessageType.SUCCESS.value: '\033[92m',
            MessageType.WARNING.value: '\033[93m',
            MessageType.FAIL.value: '\033[91m',
        }.get(message_type)
        sys.stderr.write(
            ''.join([color, message, '\r\033[0m']) if color else message)
        sys.stderr.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.finish()
