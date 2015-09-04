# -*- coding:utf-8 -*-


class Widget(object):

    def get_str(self, context):
        raise NotImplementedError


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
