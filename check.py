# -*- coding:utf-8 -*-

from time import sleep

from progress_bar.commandline import CommandLineProgressBar, widget


def main():
    widgets = [widget.Bar(under=' '), widget.Percentage(), widget.Num()]
    format_str = '{} {} ({})'
    CommandLineProgressBar.iteration(
        range(100),
        lambda item: sleep(0.01),
        widgets=widgets,
        format_str=format_str)

    with CommandLineProgressBar(100) as progress_bar:
        for _item in range(100):
            sleep(0.01)
            progress_bar.forward()


if __name__ == '__main__':
    main()
