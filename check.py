# -*- coding:utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from time import sleep

from light_progress.commandline import Loading, ProgressBar, widget


def test_default():
    print('test_default')
    with ProgressBar(100) as progress_bar:
        for item in range(100):
            sleep(0.01)
            progress_bar.forward()

    assert progress_bar.progress == 1.0


def test_iteration():
    print('test_iteration')
    ProgressBar.iteration(range(100), lambda item: sleep(0.01))


def test_generation():
    print('test_generataion')
    for item in ProgressBar.generation(range(100)):
        sleep(0.01)


def test_widget():
    print('test_widget (iteration)')
    widgets = [widget.Bar(under=' '), widget.Percentage(), widget.Num()]
    format_str = '{} {} ({})'
    ProgressBar.iteration(
        range(100),
        lambda item: sleep(0.01),
        widgets=widgets,
        format_str=format_str)


def test_error():
    print('test_error')
    try:
        with ProgressBar(100) as progress_bar:
            for item in range(100):
                sleep(0.01)
                if item >= 70:
                    raise Exception('test error')
                progress_bar.forward()
    except Exception as e:
        pass

    assert progress_bar.progress == 0.7


def test_loading():
    print('test_loading (iteration)')
    with Loading(100) as loading:
        for item in range(100):
            sleep(0.01)
            loading.forward()


def main():
    test_default()
    test_iteration()
    test_generation()
    test_widget()
    test_error()
    test_loading()


if __name__ == '__main__':
    main()
