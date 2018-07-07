# Light Progress

This is progress reporting tool for Python

```python
n = 42
with CommandLineProgressBar(n) as progress_bar:
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
progress_bar = CommandLineProgressBar(n)
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
with CommandLineProgressBar(n) as progress_bar:
    for item in range(n):
        sleep(0.01)
        progress_bar.forward()
```

### Pattern 3

Transfer iteration.

```python
from time import sleep

CommandLineProgressBar.iteration(range(42), lambda item: sleep(0.01))
```

## Colors

| status      | color |
|-------------|-------|
| In progress | Blue  |
| Success     | Green |
| Failur      | Red   |

## Widgets

`CommandLineProgressBar` can change the display format using `widget`.

```python
widget = [Bar(bar='=', tip='-'), Percentage(), Num()]
CommandLineProgressBar.iteration(range(42), lambda item: sleep(0.01), widgets=widget)

# [===============-...............] 50% (21/42)
```

```python
widget = [Percentage(), Num(), Bar(bar='#', tip='>')]
CommandLineProgressBar.iteration(range(42), lambda item: sleep(0.01), widgets=widget)

# 50% (21/42) [###############>...............]
```
