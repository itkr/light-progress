# -*- coding:utf-8 -*-

import sys


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

    def _get_str(self):
        bar = int(self.LENGTH * self.progress)
        return '[{bar}{tip}{base}] {progress}% ({current}/{max})'.format(
            bar=(self.BAR * bar),
            tip=(self.TIP if bar < self.LENGTH else self.BAR),
            base=self.BASE * (self.LENGTH - bar),
            progress=int(self.progress * 100),
            current=self.current_num,
            max=self.max_num)

    def is_finished(self):
        return self.max_num <= self.current_num

    def forward(self):
        self.current_num = min(self.max_num, self.current_num + self.unit_num)
        self.echo(self._get_str(), 'OK')

    def back(self):
        self.current_num = max(0, self.current_num - self.unit_num)
        self.echo(self._get_str(), 'OK')

    def echo(self, message, message_type=None):
        color = {
            'OK': '\033[94m',
            'SUCCESS': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
        }.get(message_type)
        sys.stderr.write(
            ''.join([color, message, '\r\033[0m']) if color else message)
        sys.stderr.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.is_finished():
            self.echo(self._get_str(), 'FAIL')
        self.echo('\n')
