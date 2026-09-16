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

### 2. `a.sort()` vs `sorted(a)` — 헷갈리면 답이 `None` 이 된다

```python
a = list(map(int, input().split()))
a.sort()          # a 자체를 정렬한다
```

```python
a = a.sort()          # ✗ a 가 None 이 된다! 최다 실수
a.sort()              # ✓ 원본이 정렬된다
a = sorted(a)         # ✓ 새 리스트를 받는다
```

`sort()` 는 **원본을 바꾸고 아무것도 돌려주지 않는다**(`None` 반환).
`sorted()` 는 **원본을 두고 새 리스트를 만들어 돌려준다.**

`sorted()` 는 리스트가 아닌 것도 받아서 리스트로 만들어준다.
```python
a = sorted(map(int, input().split()))    # 변환 + 정렬을 한 번에 (list() 불필요)
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

### 4. 질의를 줄 단위로 반복해서 읽기

```python
for _ in range(q):
    lo, hi = map(int, input().split())
```

질의 개수만큼 반복하면서 **한 줄씩** 읽는다. `_` 는 "몇 번째인지 안 쓴다"는 표시.

읽는 줄 수가 정확히 맞아야 한다. 하나라도 덜 읽거나 더 읽으면 그 뒤가 전부 밀려서
`ValueError` 가 나거나 조용히 엉뚱한 답이 나온다.

### 5. 출력 모아서 한 번에

```python
answers = []
for ...:
    answers.append(답)
print("\n".join(map(str, answers)))
```

`print` 를 20만 번 부르면 그것만으로 몇 초가 날아간다.

`join` 은 **문자열만** 받는다. 숫자 리스트면 반드시 `map(str, ...)` 을 거칠 것.
```python
"\n".join([1, 2, 3])              # ✗ TypeError: expected str, int found
"\n".join(map(str, [1, 2, 3]))    # ✓ "1\n2\n3"
```
