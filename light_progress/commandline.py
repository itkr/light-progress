# -*- coding:utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import sys
import threading
from time import sleep

from . import widget
from .core import Progress


class Colors():
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


class MessageType():
    COMPLETE = 'COMPLETE'
    COURSE = 'COURSE'
    WARNING = 'WARNING'
    FAIL = 'FAIL'


class ProgressBar(Progress):

    default_widgets = [widget.Bar(), widget.Percentage(), widget.Num(),
                       widget.StartedAt(), '-', widget.FinishedAt()]

    default_colors = {
        MessageType.COMPLETE: Colors.GREEN,
        MessageType.COURSE: Colors.BLUE,
        MessageType.WARNING: Colors.YELLOW,
        MessageType.FAIL: Colors.RED,
    }

    def __init__(self, max_num, unit_num=1, widgets=[], format_str=None, colors=None):
        self.widgets = widgets or self.default_widgets
        self.format_str = format_str or '{} ' * len(self.widgets)
        self.colors = self.default_colors.copy()
        if colors:
            self.colors.update(colors)
        super(ProgressBar, self).__init__(max_num, unit_num)

    def update(self, num):
        super(ProgressBar, self).update(num)
        if not self.is_complete():
            self._write_course()

    def finish(self):
        super(ProgressBar, self).finish()
        self._write_complete() if self.is_complete() else self._write_fail()
        self._line_brake()

    def _get_str(self):
        return self.format_str.format(
            *[wid.get_str(self) if isinstance(
                wid, widget.Widget) else str(wid) for wid in self.widgets])

    def _decolate_text(self, message, message_type=None):
        color = self.colors.get(message_type, '')
        message_format = ''.join(['\r', color, '{message}', Colors.RESET])
        return message_format.format(message=message)

    def _write(self, message, message_type=None):
        sys.stdout.write(self._decolate_text(message, message_type))
        sys.stdout.flush()

    def _write_complete(self):
        self._write(self._get_str(), MessageType.COMPLETE)

    def _write_course(self):
        self._write(self._get_str(), MessageType.COURSE)

    def _write_warning(self):
        self._write(self._get_str(), MessageType.WARNING)

    def _write_fail(self):
        self._write(self._get_str(), MessageType.FAIL)

    def _line_brake(self):
        self._write('\n')


class Loading(ProgressBar):

    default_widgets = [widget.Spinner(), widget.Num()]

    def start(self):
        self.elements_cursor = 0
        super(Loading, self).start()
        self.loop = threading.Thread(target=self._loop)
        self.loop.start()

    def _loop(self):
        while not self.finished_at:
            self._write_course()
            self.elements_cursor += 1
            sleep(0.1)
