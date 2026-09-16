# Q04. 벽 부수고 이동하기 ⭐⭐⭐⭐ (골드 / 상태 BFS) 🔥

## 문제
N×M 격자 지도에서 로봇이 이동한다. `0` 은 빈 칸, `1` 은 벽이다.
로봇은 **상하좌우**로만 움직인다.

로봇은 벽을 **최대 K번까지 부수고 지나갈 수 있다.**
(1)이던 칸을 부수면 그 칸으로 들어갈 수 있고, 부순 횟수가 1 늘어난다.

`(1, 1)` 에서 출발해 `(N, M)` 까지 가는 **최단 경로의 칸 수**를 출력하라.
(시작 칸과 도착 칸을 **모두 포함**해서 센다. 즉 시작=도착이면 1)

도달할 수 없으면 `-1` 을 출력한다.
시작 칸과 도착 칸도 벽일 수 있고, 그 경우 부수기 횟수를 소모한다.

## 입력
- 첫째 줄: N, M, K  (1 ≤ N, M ≤ 300 / 0 ≤ K ≤ 10)
- 다음 N개의 줄: 0과 1로 이루어진 길이 M의 문자열 (**공백 없음**)

## 출력
- 최단 경로의 칸 수, 불가능하면 -1

## 예제 입력
```
6 4 1
0100
1110
1000
0000
0111
0000
```

## 예제 출력
```
15
```

## 예제 입력 2
```
4 4 0
0111
1111
1111
1110
```
## 예제 출력 2
```
-1
```
> 부술 수 없으니(K=0) 벽에 막혀 도달 불가

## 예제 입력 3
```
4 4 1
0000
1101
1110
1000
```
## 예제 출력 3
```
7
```
> 위쪽 줄을 따라 (1,1)→(1,2)→(1,3)→(1,4) 로 간 뒤,
> 벽인 (2,4)를 **한 번 부수고** (3,4)→(4,4). 총 7칸.
> K=0 이었다면 같은 지도에서 -1 이다.

## 접근법 — 상태를 늘린 BFS

### 왜 그냥 BFS 로는 안 되는가
보통 BFS 는 `visited[r][c]` 하나로 "이 칸 와봤음" 을 기록한다.
그런데 이 문제에선 **같은 칸이라도 "벽을 몇 번 부수고 왔는가" 에 따라 가치가 다르다.**

```
(3,3) 에 벽 2개 부수고 먼저 도착  -> 방문 처리됨
(3,3) 에 벽 0개 부수고 나중에 도착 -> "이미 가봤네" 하고 버린다  ← 틀림!
```
0개 부수고 온 쪽이 앞으로 훨씬 유리하다. 버리면 안 된다.

### 해결: 방문 배열에 차원을 하나 더 붙인다
```
visited[r][c][k]   # (r,c) 에 "벽을 k번 부순 상태" 로 와봤는가
```
상태 개수 = N × M × (K+1) = 300 × 300 × 11 ≈ 100만.
BFS 는 각 상태를 한 번씩만 처리하니까 **O(N·M·K)** 로 끝난다.

### 이동 규칙
큐에서 `(r, c, k, dist)` 를 꺼내고, 네 방향 `(nr, nc)` 마다:
```
격자 밖이면 버린다
grid[nr][nc] == 0  이고  visited[nr][nc][k]  가 아직이면
        -> 그대로 이동 (k 유지), dist+1 로 push
grid[nr][nc] == 1  이고  k < K  이고  visited[nr][nc][k+1] 이 아직이면
        -> 벽을 부수고 이동 (k+1), dist+1 로 push
```

**BFS 라서 큐에서 처음 꺼낸 순간이 곧 최단거리**다. (모든 간선 비용이 1)
push 할 때 바로 visited 를 켜야 한다 — 꺼낼 때 켜면 같은 상태가 큐에 중복으로 쌓인다.

## 함정 ⚠️
- 입력이 `0100` 처럼 **붙어서** 들어온다. `split()` 말고 문자열을 그대로 인덱싱
- 시작 칸이 벽일 수 있다 → 시작 상태의 k를 0이 아니라 **1로** 시작해야 한다 (K=0이면 -1)
- N=M=1 이면 답은 1 (시작이 벽이면 K≥1일 때만 1, 아니면 -1)
- `collections.deque` 를 써라. 리스트의 `pop(0)` 은 O(N)이라 터진다

## 채점
```
python training/quiz/judge.py hard01_wall_break
```

---

## English version

### Q04. Breaking Walls (hard / BFS over an extended state)

You are given an N×M grid of `0` (empty) and `1` (wall). Starting from the top-left
cell `(1, 1)`, move **up/down/left/right** to reach the bottom-right cell `(N, M)`.
You may **break at most K walls** along the way; entering a wall cell costs one break.

Print the **number of cells on the shortest path**, counting both the start and the
destination cell. Print `-1` if the destination is unreachable. The start and the
destination themselves may be walls (breaking them also costs one).

**Input** — The first line contains N, M, K (1 ≤ N, M ≤ 300; 0 ≤ K ≤ 10).
Each of the next N lines contains a string of M characters, `0` or `1`, **with no spaces**.

**Output** — The length of the shortest path, or -1.

**Sample Input**
```
6 4 1
0100
1110
1000
0000
0111
0000
```
**Sample Output**
```
15
```

**Approach** — Plain BFS is wrong because the same cell reached with *fewer* breaks
used is strictly better. Add the number of breaks to the state: `visited[r][c][k]`.
Each of the N·M·(K+1) states is expanded once, so the whole search is O(N·M·K).

> 단어장: grid / cell(칸) / adjacent(인접한) / unreachable(도달 불가능한)
> / at most K times(최대 K번) / shortest path(최단 경로) / state(상태) / queue(큐)
