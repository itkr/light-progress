# -*- coding:utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals


class Widget(object):

    def get_str(self, context):
        raise NotImplementedError


class Bar(Widget):

    def __init__(self, length=30, bar='█', tip='▉', under='.', before='[', after=']'):
        self.before = before
        self.after = after
        self.length = length
        self.bar = bar
        self.tip = tip
        self.under = under

    def get_str(self, context):
        bar_length = int(self.length * context.progress)
        return '{before}{bar}{tip}{under}{after}'.format(
            before=self.before,
            bar=self.bar * bar_length,
            tip=self.tip if bar_length < self.length else self.bar,
            under=self.under * (self.length - bar_length),
            after=self.after)


class Percentage(Widget):

    def __init__(self, percent='%'):
        self.percent = percent

    def get_str(self, context):
        return '{percentage}{percent}'.format(
            percentage=int(context.percentage), percent=self.percent)


class Num(Widget):

    def __init__(self, separate='/'):
        self.separate = separate

    def get_str(self, context):
        return '{current}{separate}{max}'.format(
            current=context.current_num,
            separate=self.separate,
            max=context.max_num)


class StartedAt(Widget):

    def get_str(self, context):
        return '{}'.format(context.started_at or '')


class FinishedAt(Widget):

    def get_str(self, context):
        return '{}'.format(context.finished_at or '')


class ElapsedSeconds(Widget):

    def get_str(self, context):
        return '{}'.format(context.elapsed_seconds)


class Spinner(Widget):

    def __init__(self, elements=('-', '\\', '|', '/'), success='*', failure='*'):
        self.elements = elements
        self.success = success
        self.failure = failure

    def get_str(self, context):
        if context.finished_at:
            return self.success if context.is_complete() else self.failure
        return self.elements[context.elements_cursor % len(self.elements)]
