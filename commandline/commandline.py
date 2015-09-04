# -*- coding:utf-8 -*-

import sys

import enum

from progress_bar import ProgressBar
from . import widget


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
        self.widgets = widgets or [
            widget.Bar(), widget.Percentage(), widget.Num(),
            widget.StartedAt(), '-', widget.FinishedAt()]
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
        return ' '.join([wid.get_str(self) if isinstance(wid, widget.Widget)
                         else str(wid) for wid in self.widgets])

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
