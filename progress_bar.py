# -*- coding:utf-8 -*-

import sys


class ProgressBar(object):

    LENGTH = 30

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
            bar=('=' * bar),
            tip=('>' if bar < self.LENGTH else ''),
            base='.' * (self.LENGTH - bar),
            progress=int(self.progress * 100),
            current=self.current_num,
            max=self.max_num)

    def is_end(self):
        return self.max_num <= self.current_num

    def forward(self):
        self.current_num = min(self.max_num, self.current_num + self.unit_num)
        self.echo()

    def back(self):
        self.current_num = max(0, self.current_num - self.unit_num)
        self.echo()

    def echo(self):
        sys.stderr.write('\r\033[94m{}\033[0m'.format(self._get_str()))
        sys.stderr.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stderr.write('\n')
        sys.stderr.flush()
#
#
#def check():
#    from time import sleep
#    while True:
#        with ProgressBar(100) as progress_bar:
#            if progress_bar.is_end():
#                return
#            sleep(0.01)
#            progress_bar.forward()
