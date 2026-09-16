# Q04. 청소 구역 나누기 ⭐⭐⭐ (실버 / BFS 연결 요소)

## 문제
N×M 격자 지도에 먼지가 흩어져 있다. `1` 은 먼지, `0` 은 깨끗한 칸이다.

**상하좌우로 붙어 있는 먼지들은 하나의 구역**으로 친다. (대각선은 안 붙은 것으로 본다)

1. 구역이 **몇 개** 있는지
2. 가장 큰 구역의 **칸 수**

를 구하라. 먼지가 하나도 없으면 `0 0` 을 출력한다.

## 입력
- 첫째 줄: N, M  (1 ≤ N, M ≤ 500)
- 다음 N개의 줄: 0과 1로 이루어진 길이 M의 문자열 (**공백 없음**)

## 출력
- 구역 개수와 가장 큰 구역의 칸 수를 공백으로 구분해 한 줄에

## 예제 입력
```
4 5
11000
11000
00110
00011
```

## 예제 출력
```
2 4
```
> 왼쪽 위 2×2 덩어리(4칸)가 하나, 오른쪽 아래 계단 모양 덩어리(4칸)가 하나.
> 대각선으로만 닿은 건 **안 붙은 것**이다.

## 예제 입력 2
```
3 3
101
010
101
```
## 예제 출력 2
```
5 1
```
> 전부 대각선으로만 닿아서 5개 구역, 각각 1칸씩

## 접근법 — 격자를 그래프로 보기

**칸 = 정점, 상하좌우로 붙은 것 = 간선.** 그러면 "구역"은 곧 **연결 요소**다.

```
모든 칸을 하나씩 훑는다:
    이 칸이 1이고 아직 방문 안 했으면
        -> 새 구역 발견! 구역 개수 += 1
        -> 여기서 BFS 를 돌려 붙어 있는 1들을 전부 방문 처리하고 칸 수를 센다
        -> 가장 큰 구역 갱신
```

바깥 이중 for문이 있어서 O(N·M·N·M) 같아 보이지만, **각 칸은 딱 한 번만 BFS에 들어간다**
(방문 처리했으니까). 그래서 전체 **O(N·M)**.

### BFS 한 덩어리 세는 코드 모양
```python
from collections import deque

q = deque()
q.append((r, c))
visited[r][c] = True        # 넣을 때 바로 방문 처리!
size = 0
while q:
    y, x = q.popleft()
    size += 1
    for dy, dx in ((1,0), (-1,0), (0,1), (0,-1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < n and 0 <= nx < m and not visited[ny][nx] and grid[ny][nx] == '1':
            visited[ny][nx] = True
            q.append((ny, nx))
```

## 함정 ⚠️
- **방문 처리는 큐에 넣을 때** 해야 한다. 꺼낼 때 하면 같은 칸이 큐에 여러 번 들어가서
  size 가 부풀려지고 느려진다. 이게 BFS 최대 실수
- 재귀 DFS 로 짜면 500×500 = 25만 깊이까지 들어갈 수 있어서 **RecursionError**.
  `sys.setrecursionlimit` 을 올려도 파이썬은 터진다. **BFS(deque)로 짤 것**
- `0 <= ny < n` 같은 범위 체크를 **배열 접근보다 먼저** 해야 한다 (`and` 의 단락 평가)
- 입력이 `11000` 처럼 붙어서 들어온다. 문자열 그대로 인덱싱하면 된다

## 채점
```
python training/quiz/judge.py q04_clean_zone
```

---

## English version

### Q04. Counting Regions (medium / BFS, connected components)

You are given an N×M grid of `0` and `1`. Cells containing `1` that are **adjacent
horizontally or vertically** belong to the same region (diagonals do **not** connect).

Print the **number of regions** and the **size of the largest region**, separated by a
space. If there are no `1` cells, print `0 0`.

**Input** — The first line contains N and M (1 ≤ N, M ≤ 500). Each of the next N lines
contains a string of M characters, `0` or `1`, with no spaces.

**Output** — Two integers: the region count and the largest region size.

**Sample Input**
```
4 5
11000
11000
00110
00011
```
**Sample Output**
```
2 4
```

**Approach** — Treat each cell as a vertex and each side-adjacency as an edge; a region
is a **connected component**. Scan every cell; when you meet an unvisited `1`, run a BFS
from it, marking cells visited **as you push them** onto the queue, and count how many
cells that BFS reaches. Each cell is enqueued at most once, so the total is O(N·M).

> 단어장: adjacent(인접한) / horizontally and vertically(상하좌우로)
> / connected component(연결 요소) / region(구역) / traverse(순회하다) / enqueue(큐에 넣다)
