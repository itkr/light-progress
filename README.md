# Progress bar

## example

### a

```
from time import sleep

with ProgressBar(256, 1) as progress_bar:
    while True:
        if progress_bar.is_finished():
            return
        sleep(0.01)
        progress_bar.forward()
```

### b

```
from time import sleep

n = 256
with ProgressBar(n) as progress_bar:
    for i in range(n):
        sleep(0.01)
        progress_bar.forward()
```

## result

```
[-..............................] 1% (1/256)
[===============-...............] 50% (128/256)
[===============================] 100% (256/256)
```
