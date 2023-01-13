# -*- coding:utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

from time import sleep

from light_progress.commandline import (
    Colors,
    Loading,
    MessageType,
    ProgressBar,
    puts,
    widget,
)


def test_default():
    print("test_default")
    with ProgressBar(100) as progress_bar:
        for item in range(100):
            sleep(0.01)
            progress_bar.forward()

    assert progress_bar.progress == 1.0


def test_puts():
    print("test_puts")
    for item in ProgressBar.generation(range(100)):
        sleep(0.01)
        if item % 20 == 0:
            puts(item)

    print("test_puts")
    with ProgressBar(100) as progress_bar:
        for item in range(100):
            sleep(0.01)
            progress_bar.forward()
            if item % 20 == 0:
                progress_bar.puts(item)


def test_iteration():
    print("test_iteration")
    ProgressBar.iteration(range(100), lambda item: sleep(0.01))


def test_generation():
    print("test_generataion")
    for item in ProgressBar.generation(range(100)):
        sleep(0.01)


def test_widget():
    print("test_widget (iteration)")
    widgets = [
        widget.Spinner(),
        widget.Bar(under="-", tip=">", bar="*", before="|", after="|"),
        widget.Percentage(),
        widget.Num(),
    ]
    format_str = "{} {} ({})"
    ProgressBar.iteration(
        range(100), lambda item: sleep(0.01), widgets=widgets, format_str=format_str
    )


def test_colors():
    print("test_colors")
    colors = {
        MessageType.COURSE: Colors.YELLOW,
        MessageType.COMPLETE: Colors.BLUE,
    }
    ProgressBar.iteration(range(100), lambda item: sleep(0.01), colors=colors)


def test_error():
    print("test_error")
    try:
        with ProgressBar(100) as progress_bar:
            for item in range(100):
                sleep(0.01)
                if item >= 70:
                    raise Exception("test error")
                progress_bar.forward()
    except Exception as e:
        pass

    assert progress_bar.progress == 0.7


def test_loading():
    print("test_loading (iteration)")
    Loading.iteration(range(100), lambda item: sleep(0.01))


def test_loading_widget():
    print("test_loading (iteration)")
    elements = [
        "\U0001f311",
        "\U0001f312",
        "\U0001f313",
        "\U0001f314",
        "\U0001f315",
        "\U0001f316",
        "\U0001f317",
        "\U0001f318",
    ]
    widgets = [
        widget.Spinner(elements=elements, success="🌝", failure="🌚"),
        widget.Num(),
    ]
    Loading.iteration(range(100), lambda item: sleep(0.01), widgets=widgets)

    elements = [
        "\U0001f550",
        "\U0001F55C",
        "\U0001F551",
        "\U0001F55D",
        "\U0001F552",
        "\U0001F55E",
        "\U0001F553",
        "\U0001F55F",
        "\U0001F554",
        "\U0001F560",
        "\U0001F555",
        "\U0001F561",
        "\U0001F556",
        "\U0001F562",
        "\U0001F557",
        "\U0001F563",
        "\U0001F558",
        "\U0001F564",
        "\U0001F559",
        "\U0001F565",
        "\U0001F55A",
        "\U0001F566",
        "\U0001F55B",
        "\U0001F567",
    ]
    widgets = [
        widget.Spinner(elements=elements, success="✔︎", failure="❌"),
        widget.Num(),
        widget.ElapsedSeconds(),
    ]
    Loading.iteration(range(100), lambda item: sleep(0.01), widgets=widgets)


def main():
    test_default()
    test_iteration()
    test_generation()
    test_puts()
    test_widget()
    test_colors()
    test_error()
    test_loading()
    test_loading_widget()


if __name__ == "__main__":
    main()
