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

### 3. 갈 수 없는 이유를 한 줄씩 걸러내기

```python
if nr < 0 or nr >= n:
    continue
if nc < 0 or nc >= m:
    continue
```

조건을 `and` 로 길게 잇는 대신 `continue` 로 하나씩 쳐낸다.
어느 조건에서 걸렸는지 눈으로 바로 보이고, 주석도 이유별로 달 수 있다.
(자세한 건 [SYNTAX.md 7번](../SYNTAX.md))

### 4. 답을 변수에 담고 `break` 로 빠져나오기

```python
answer = -1

while q:
    ...
    if r == n - 1 and c == m - 1:
        answer = dist
        break          # 최단거리를 찾았으니 더 돌 필요가 없다
    ...

print(answer)
```

BFS는 **처음 도달했을 때가 최단**이므로 즉시 멈춰야 한다.

`answer` 를 미리 `-1` 로 두는 게 핵심이다. 큐가 다 비도록 도착을 못 하면
`answer` 가 `-1` 그대로 남아서 **"도달 불가"가 자동으로 출력**된다.
if/else 로 나눌 필요가 없어진다.

```python
# ✗ 찾았을 때 바로 print 하면, 못 찾은 경우를 따로 처리해야 해서 코드가 갈라진다
# ✓ 변수에 담아두고 마지막에 한 번만 print
```

### 5. 시작 칸이 벽인 경우 처리

```python
if grid[0][0] == '1':
    start_b = 1        # 시작부터 한 번 부수고 출발
else:
    start_b = 0

if start_b <= k:       # 부술 횟수가 없으면 출발조차 못 한다
    ...BFS...
```

`start_b` 를 먼저 정하고, BFS 전체를 `if` 안에 넣어 **출발 자체가 불가능한 경우**를 걸러낸다.
이런 "시작/끝 자체가 예외" 케이스는 히든 테스트에 거의 항상 들어있다.
