# Progress bar

## example

### 1

```
from time import sleep

ProgressBar.iteration(range(42), lambda item: sleep(0.01 * item))
```

### 2

```
from time import sleep

n = 42
with ProgressBar(n) as progress_bar:
    for item in range(n):
        sleep(0.01 * item)
        progress_bar.forward()
```

### 3

```
from time import sleep

n = 42
progress_bar = ProgressBar(n)
progress_bar.start()
for item in range(n):
    sleep(0.01 * item)
    progress_bar.forward()
progress_bar.finish()
```

## result

```
[-..............................] 1% (1/42)
[===============-...............] 50% (21/42)
[===============================] 100% (42/42)
```
