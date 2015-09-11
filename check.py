# -*- coding:utf-8 -*-

from time import sleep
from commandline import CommandLineProgressBar, widget


def main():
    widgets = [widget.Bar(bar='-'), widget.Percentage(), widget.Num()]
    format_str = '{} {} ({})'
    CommandLineProgressBar.iteration(
        range(100),
        lambda item: sleep(0.01),
        widgets=widgets,
        format_str=format_str)


if __name__ == '__main__':
    main()
