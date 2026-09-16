# hard01 파이썬 문법 노트 🐍

> 공통 문법은 [`SYNTAX.md`](../SYNTAX.md) 참고.
> BFS 기본 문법(`deque`, 방향 배열, 2차원 리스트)은 [`q04_clean_zone/syntax.md`](../q04_clean_zone/syntax.md) 에 있다.

## 이 문제에 나오는 문법

### 1. 3차원 리스트 만들기

```python
visited = [[[False] * (k + 1) for _ in range(m)] for _ in range(n)]
```

컴프리헨션을 **안에서 바깥으로** 읽으면 이해가 쉽다.

```
[False] * (k+1)              →  길이 k+1 짜리 한 줄          visited[r][c]
[... for _ in range(m)]      →  그게 m개                     visited[r]
[... for _ in range(n)]      →  그게 n개                     visited
```

접근은 `visited[행][열][부순횟수]` 순서. 만든 순서와 인덱스 순서가 **반대**라는 게 헷갈리는 지점 —
바깥 컴프리헨션이 가장 앞 인덱스가 된다.

2차원과 마찬가지로 `[[[False] * a] * b] * c` 는 전부 같은 객체를 가리켜서 **버그**다.

### 2. 4개짜리 튜플 언패킹

```python
q.append((0, 0, start_b, 1))
...
r, c, b, dist = q.popleft()
```

큐에 담는 게 좌표만이 아니라 **"상태 전체"** 다. 몇 개든 개수만 맞으면 언패킹된다.
개수가 틀리면 `ValueError: not enough values to unpack`.

상태가 더 늘어나면 튜플 대신 이름을 붙이는 방법도 있다(가독성 ↑, 속도는 ↓):
```python
from collections import namedtuple
State = namedtuple('State', 'r c b dist')
q.append(State(0, 0, start_b, 1))
s = q.popleft()
s.r, s.b        # 이름으로 접근
```

### 3. `not (...)` 로 조건 뒤집기

```python
if not (0 <= nr < n and 0 <= nc < m):
    continue
```

"범위 안에 있다"를 만들고 `not` 으로 뒤집어 **"범위 밖이면 건너뛴다"** 로 쓴다.
직접 뒤집어 쓰는 것보다 실수가 적다.

```python
if nr < 0 or nr >= n or nc < 0 or nc >= m:     # 같은 뜻이지만 부등호 4개를 다 뒤집어야 한다
```

드모르간 법칙: `not (A and B)` = `(not A) or (not B)`. 괄호를 빼먹으면 뜻이 완전히 달라진다.

### 4. `return` 으로 즉시 탈출

```python
def main():
    ...
    while q:
        if r == n - 1 and c == m - 1:
            print(dist)
            return          # 함수를 즉시 끝낸다. 아래 print(-1) 은 실행 안 됨
    print(-1)
```

BFS는 **처음 도달했을 때가 최단**이므로 더 돌 이유가 없다.
`break` 는 루프만 빠져나와서 아래 `print(-1)` 까지 실행되어 **답이 두 번 찍힌다**.

`return` 을 쓰려면 코드가 함수 안에 있어야 한다. `def main()` 으로 감싸는 또 다른 이유다.

### 5. 조건부 표현식으로 초깃값 정하기

```python
start_b = 1 if grid[0][0] == '1' else 0
if start_b > k:
    print(-1)
    return
```

시작 칸이 벽일 수도 있다는 예외를 **한 줄로** 처리한 것.
이런 "시작/끝 자체가 예외" 케이스는 히든 테스트에 거의 항상 들어있다.
