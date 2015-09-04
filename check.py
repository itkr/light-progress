# -*- coding:utf-8 -*-

from time import sleep
from commandline import CommandLineProgressBar, widget


def main():
    widgets = [widget.Bar(), widget.Percentage(), widget.Num()]
    CommandLineProgressBar.iteration(
        range(100), lambda item: sleep(0.01), widgets=widgets)


if __name__ == '__main__':
    main()
