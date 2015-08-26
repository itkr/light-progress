# Progress bar

## example

```
from time import sleep

with ProgressBar(100, 1) as progress_bar:
    while True:
        if progress_bar.is_finished():
            return
        sleep(0.01)
        progress_bar.forward()
```

## result

```
[>..............................] 1% (1/100)
[===============>...............] 50% (50/100)
[==============================] 100% (100/100)
```
