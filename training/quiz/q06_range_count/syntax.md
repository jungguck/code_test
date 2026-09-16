# Q06 파이썬 문법 노트 🐍

> 공통 문법(출력 빠르게 하기 등)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. `from X import a, b` — 필요한 것만 가져오기

```python
from bisect import bisect_left, bisect_right
```

`import bisect` 로 가져오면 매번 `bisect.bisect_left(...)` 라고 써야 하는데,
`from` 으로 가져오면 **이름만으로** 부를 수 있다.

```python
import bisect
bisect.bisect_left(a, x)        # 모듈 이름을 거쳐서 찾는다 (아주 조금 느리다)

from bisect import bisect_left
bisect_left(a, x)               # 바로 찾는다
```

20만 번 호출하면 이 차이가 쌓인다. `from collections import deque` 도 같은 이유.

### 2. `sorted(map(int, ...))` — 변환과 정렬을 한 번에

```python
a = sorted(map(int, data[2:2 + n]))
```

`sorted()` 는 **반복 가능한 무엇이든 받아서 새 리스트를 반환**한다.
그래서 `list()` 로 감쌀 필요가 없다 — `sorted` 가 알아서 리스트를 만든다.

```python
sorted(map(int, [b'3', b'1']))        # ✓ [1, 3]
list(map(int, ...)).sort()            # ✗ None 이 된다 (sort 는 반환값이 없다)
```

| | 원본 | 반환 |
|---|---|---|
| `a.sort()` | **바뀐다** | `None` |
| `sorted(a)` | 그대로 | **새 리스트** |

### 3. `bisect_left` vs `bisect_right` ⭐

```python
a = [1, 2, 3, 5, 5, 8, 9]
bisect_left(a, 5)     # → 3   "5 가 들어갈 가장 왼쪽 자리" = 5 이상인 첫 위치
bisect_right(a, 5)    # → 5   "5 가 들어갈 가장 오른쪽 자리" = 5 초과인 첫 위치
```

```
인덱스:  0  1  2  3  4  5  6
값:      1  2  3  5  5  8  9
                  ↑     ↑
             left=3   right=5
             (5들의 앞)  (5들의 뒤)
```

**둘의 차이가 곧 그 값의 개수**다.
```python
bisect_right(a, 5) - bisect_left(a, 5)      # → 2   (5가 두 개)
```

값이 배열에 없으면 둘이 같은 값을 준다. 그래서 "있는지 확인"은 이렇게 한다:
```python
i = bisect_left(a, x)
있다 = i < len(a) and a[i] == x      # 범위 체크가 먼저! (단락 평가)
```

**반드시 정렬된 리스트여야 한다.** 안 되어 있으면 에러 없이 엉뚱한 값을 준다.

### 4. 수동 인덱스 포인터로 입력 읽기

```python
p = 2 + n
for _ in range(q):
    lo = int(data[p])
    hi = int(data[p + 1])
    p += 2
```

토큰을 통째로 읽었기 때문에 **지금 어디까지 읽었는지**를 직접 들고 있어야 한다.
`p` 를 정확히 소비한 만큼(`+= 2`) 올리는 게 핵심. 이걸 틀리면 `ValueError` 가 나거나
조용히 엉뚱한 답이 나온다.

`zip` 으로 두 개씩 짝지어 도는 방법도 있다:
```python
qs = data[2 + n:]
for lo, hi in zip(qs[0::2], qs[1::2]):      # 짝수 번째, 홀수 번째를 짝지어서
    ...
```
`a[시작::간격]` 은 **확장 슬라이싱**. `qs[0::2]` 는 0,2,4... 번째를 뽑는다.

### 5. 출력 모아서 한 번에

```python
out = []
for ...:
    out.append(답)
sys.stdout.write("\n".join(map(str, out)) + "\n")
```

`print` 를 20만 번 부르면 그것만으로 몇 초가 날아간다.

`join` 은 **문자열만** 받는다. 숫자 리스트면 반드시 `map(str, ...)` 을 거칠 것.
```python
"\n".join([1, 2, 3])              # ✗ TypeError: expected str, int found
"\n".join(map(str, [1, 2, 3]))    # ✓ "1\n2\n3"
```
