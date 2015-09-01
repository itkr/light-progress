# Progress bar

## example

ProgressBarは大きく分けて３つのパターンが使えます。しかし、最もスマートに書けるのは３つ目のパターンなのでその使用を推奨します。

### パターン1

直感的な処理のパターンです。ProgressBarのインスタンスを作り、処理の前後でそれぞれ`start`と`finish`を呼びます。プログレスバーを進めるときに`foward`を呼びます。

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

### パターン2

パターン1では明示的に`start`と`finish`を呼び出していますが、処理を忘れてしまう可能性があります。その場合はwithを使うことでそれらの呼び出しを省略できます。

```
from time import sleep

n = 42
with ProgressBar(n) as progress_bar:
    for item in range(n):
        sleep(0.01 * item)
        progress_bar.forward()
```

### パターン3

操作対象のオブジェクトがIterableである場合は、`iteration`を用いてProgressBarにイテレーションを委譲することでコードをより簡潔に書くことが出来ます。

```
from time import sleep

ProgressBar.iteration(range(42), lambda item: sleep(0.01 * item))
```

## result

```
[-..............................] 1% (1/42)
[===============-...............] 50% (21/42)
[===============================] 100% (42/42)
```
