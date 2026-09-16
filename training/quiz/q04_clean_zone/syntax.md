# Q04 파이썬 문법 노트 🐍

> 공통 문법(`and` 단락 평가, 연쇄 비교 등)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. ⚠️ 2차원 리스트 만들기 — 파이썬 최대 함정

```python
visited = [[False] * m for _ in range(n)]      # ✓ 정답
visited = [[False] * m] * n                    # ✗ 버그!
```

`* n` 은 **같은 리스트를 n번 복사하는 게 아니라, 같은 리스트를 n번 가리킨다.**

```python
bad = [[False] * 3] * 2
bad[0][0] = True
print(bad)        # [[True, False, False], [True, False, False]]
#                                            ↑ 건드리지도 않은 줄이 같이 바뀐다
```

`[[False] * m for _ in range(n)]` 은 **매 반복마다 새 리스트를 만들어서** 안전하다.
1차원(`[0] * m`)은 숫자가 불변이라 이 문제가 없다. **2차원부터 조심.**

### 2. 문자열 줄을 그대로 격자로 쓰기

```python
grid = []
for _ in range(n):
    grid.append(input())
```

`input()` 은 **줄 끝 개행을 알아서 떼어주기 때문에** 읽은 줄을 그대로 쓰면 된다.

```python
# 입력 줄이 "11000" 일 때
row = input()      # '11000'   길이 5  ✓
row[0]             # '1'
```

문자열은 리스트처럼 인덱싱이 되므로, 2차원 리스트로 바꿀 필요가 없다.
```python
grid[r][c]         # r번째 줄의 c번째 글자
```
(문자열은 수정이 안 되지만, 이 문제는 읽기만 하므로 상관없다)

### 3. `deque` — BFS 전용 큐

```python
from collections import deque

q = deque()
q.append((sr, sc))      # 뒤에 넣기    O(1)
r, c = q.popleft()      # 앞에서 빼기  O(1)
while q:                # 큐가 빌 때까지
```

리스트로도 되지만 **`list.pop(0)` 은 O(N)** 이다. 앞을 빼면 나머지를 전부 한 칸씩
당겨야 하기 때문. 25만 칸짜리 BFS에서 이걸 쓰면 시간 초과가 난다.

```python
q.pop(0)        # ✗ 리스트: O(N) → 전체 O(N²)
q.popleft()     # ✓ deque:  O(1)
```

`deque` 는 양쪽 끝이 다 O(1)이라 `appendleft` / `pop` 도 있다(0-1 BFS 에서 쓴다).

### 4. 방향 배열 — 튜플의 튜플을 순회

```python
for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
    nr = r + dr
    nc = c + dc
```

상하좌우를 네 번 복붙하는 대신 **방향을 데이터로** 만들어 한 번에 돈다.
`dr` 은 row 변화량, `dc` 는 column 변화량(`d` 는 delta, 변화량).

대각선까지 8방향으로 늘리려면 이 튜플만 고치면 된다 — 나머지 코드는 그대로.
```python
DIRS = ((1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1))
```

### 5. `continue` 로 빨리 걸러내기

```python
if grid[sr][sc] != '1' or visited[sr][sc]:
    continue
```

`continue` 는 **이번 반복만 건너뛰고 다음 반복으로** 간다 (`break` 는 루프를 완전히 탈출).

이렇게 "아닌 경우"를 위에서 먼저 쳐내면 아래 코드의 들여쓰기가 한 단계 줄어든다.
중첩이 깊어지는 걸 막는 방법이라 **early return / early continue** 라고 부른다.

```python
# ✗ 들여쓰기가 계속 깊어진다
for ...:
    if 조건:
        if 다른조건:
            실제_할_일

# ✓ 평평해진다
for ...:
    if not 조건: continue
    if not 다른조건: continue
    실제_할_일
```

## 이 문제에서 실수하기 쉬운 곳

```python
q.append((nr, nc))
visited[nr][nc] = True      # ✗ 꺼낼 때 방문 처리 → 같은 칸이 큐에 여러 번 들어간다
```
**큐에 넣는 순간 바로** `visited` 를 켜야 한다. BFS 버그의 90%가 여기서 나온다.
