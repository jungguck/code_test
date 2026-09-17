# Q09 파이썬 문법 노트 🐍

> 공통 문법(`input()`, `map`, 출력)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. 누적합 배열 만들기

```python
pre = [0] * (n + 1)                 # 길이 n+1, 앞에 0 한 칸을 둔다
for i in range(n):
    pre[i + 1] = pre[i] + a[i]
```

`pre[i]` = "앞에서 i개의 합". `pre[0] = 0` 으로 시작해
바로 앞 누적값에 현재 원소를 더해 나간다.

```
a   =    1   2   3   4   5
pre = 0  1   3   6  10  15
        ↑pre[1]      ↑pre[4]
```

### 2. 구간합은 뺄셈 한 번

```python
pre[r] - pre[l - 1]        # [l, r] 구간의 합
```

`pre[r]`(앞에서 r개) 에서 `pre[l-1]`(앞에서 l-1개) 을 빼면
**딱 l부터 r까지만** 남는다. `l-1` 때문에 `pre` 앞에 0칸을 둔 것이다.

```
[2, 3] 합 = pre[3] - pre[1] = 6 - 1 = 5
```

### 3. `sys.stdin.readline` — 빠른 입력

```python
import sys
input = sys.stdin.readline
```

`input()` 을 통째로 갈아끼우는 관용구다. 질의가 10만 줄이면
기본 `input()` 은 느려서 시간 초과가 날 수 있는데, 이걸로 바꾸면 몇 배 빨라진다.

주의: `readline` 은 **줄 끝 `\n` 을 떼지 않는다.** 숫자로 바꿀 땐 `int()`/`map(int, ...)`
가 알아서 무시하니 괜찮지만, 문자열을 그대로 쓸 땐 `.rstrip()` 이 필요할 수 있다.

### 4. 출력은 모아서 한 번에

```python
out = []
for _ in range(q):
    ...
    out.append(str(구간합))
print("\n".join(out))
```

질의마다 `print` 하면 10만 번 호출이라 느리다.
문자열 리스트에 모았다가 **`"\n".join` 으로 한 방에** 출력한다.
`join` 은 문자열만 받으므로 `str(...)` 을 씌운다. ([SYNTAX.md 3번](../SYNTAX.md))

## 함정

`pre[l - 1]` 에서 `l = 1` 이면 `pre[0] = 0` 이라 정확히 맞는다.
만약 `pre` 앞에 0칸을 안 두고 `pre[r] - pre[l]` 로 쓰면 **왼쪽 끝 원소 하나가 빠진다.**
