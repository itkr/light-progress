# -*- coding:utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import sys
import threading
from time import sleep

from . import widget
from .core import Progress


class ProgressBar(Progress):

    default_widgets = [widget.Bar(), widget.Percentage(), widget.Num(),
                       widget.StartedAt(), '-', widget.FinishedAt()]

    class MessageType():
        COMPLETE = 'COMPLETE'
        COURSE = 'COURSE'
        WARNING = 'WARNING'
        FAIL = 'FAIL'

    def __init__(self, max_num, unit_num=1, widgets=[], format_str=None):
        self.widgets = widgets or self.default_widgets
        self.format_str = format_str or '{} ' * len(self.widgets)
        super(ProgressBar, self).__init__(max_num, unit_num)

    @property
    def default_widgets(self):
        return [widget.Bar(), widget.Percentage(), widget.Num(),
                widget.StartedAt(), '-', widget.FinishedAt()]

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

    def _get_message_format(self, message_type=None):
        return {
            self.MessageType.COMPLETE: '\r\033[92m{message}\033[0m',
            self.MessageType.COURSE: '\r\033[94m{message}\033[0m',
            self.MessageType.WARNING: '\r\033[93m{message}\033[0m',
            self.MessageType.FAIL: '\r\033[91m{message}\033[0m',
        }.get(message_type) or '\r{message}'

    def _write(self, message, message_type=None):
        message_format = self._get_message_format(message_type)
        sys.stderr.write(message_format.format(message=message))
        sys.stderr.flush()

    def _write_complete(self):
        self._write(self._get_str(), self.MessageType.COMPLETE)

    def _write_course(self):
        self._write(self._get_str(), self.MessageType.COURSE)

    def _write_warning(self):
        self._write(self._get_str(), self.MessageType.WARNING)

    def _write_fail(self):
        self._write(self._get_str(), self.MessageType.FAIL)

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
