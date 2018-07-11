# -*- coding:utf-8 -*-

from time import sleep

from light_progress.commandline import ProgressBar, widget


def test_widget():
    widgets = [widget.Bar(under=' '), widget.Percentage(), widget.Num()]
    format_str = '{} {} ({})'
    ProgressBar.iteration(
        range(100),
        lambda item: sleep(0.01),
        widgets=widgets,
        format_str=format_str)


def test_default():
    with ProgressBar(100) as progress_bar:
        for item in range(100):
            sleep(0.01)
            progress_bar.forward()

    assert progress_bar.progress == 1.0


def test_error():
    try:
        with ProgressBar(100) as progress_bar:
            for item in range(100):
                sleep(0.01)
                if item >= 70:
                    raise Exception('test error')
                progress_bar.forward()
    except Exception as e:
        print(str(e))

    assert progress_bar.progress == 0.7


def main():
    test_widget()
    test_default()
    test_error()


if __name__ == '__main__':
    main()
