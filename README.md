# Light Progress

This is progress reporting tool for Python

```python
n = 42
with ProgressBar(n) as progress_bar:
    for item in range(n):
        sleep(0.01)
        progress_bar.forward()
```

```python
# [-..............................] 1% (1/42)
# [===============-...............] 50% (21/42)
# [===============================] 100% (42/42)
```

## Examples

### Pattern 1

Call `start` `forward` and `finish` yourself.

```python
from time import sleep

n = 42
progress_bar = ProgressBar(n)
progress_bar.start()

for item in range(n):
    sleep(0.01)
    progress_bar.forward()

progress_bar.finish()
```

### Pattern 2

Do iterations in `with`. `start` and `finish` do not have to be called explicitly.

```python
from time import sleep

n = 42
with ProgressBar(n) as progress_bar:
    for item in range(n):
        sleep(0.01)
        progress_bar.forward()
```

### Pattern 3

Transfer iteration.

```python
from time import sleep

ProgressBar(range(42), lambda item: sleep(0.01))
```

## Colors

| status      | color |
|-------------|-------|
| In progress | Blue  |
| Success     | Green |
| Failur      | Red   |

## Widgets

`ProgressBar` can change the display format using `widget`.

```python
widget = [Bar(bar='=', tip='-'), Percentage(), Num()]
ProgressBar.iteration(range(42), lambda item: sleep(0.01), widgets=widget)

# [===============-...............] 50% (21/42)
```

```python
widget = [Percentage(), Num(), Bar(bar='#', tip='>')]
ProgressBar.iteration(range(42), lambda item: sleep(0.01), widgets=widget)

# 50% (21/42) [###############>...............]
```
