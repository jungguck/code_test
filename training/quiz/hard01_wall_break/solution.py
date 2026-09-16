import sys
from collections import deque

input = sys.stdin.readline

n, m, k = map(int, input().split())

grid = []
for _ in range(n):
    grid.append(input().strip())

# visited[행][열][부순횟수] -- 같은 칸이라도 "몇 번 부수고 왔는지"에 따라 다른 상태다
visited = [[[False] * (k + 1) for _ in range(m)] for _ in range(n)]

# 시작 칸이 벽이면 그것부터 부수고 시작한다
if grid[0][0] == '1':
    start_b = 1
else:
    start_b = 0

answer = -1

if start_b <= k:                     # 시작부터 못 부수면 아예 출발도 못 한다
    q = deque()
    q.append((0, 0, start_b, 1))     # (행, 열, 부순횟수, 지나온 칸 수)
    visited[0][0][start_b] = True

    while q:
        r, c, b, dist = q.popleft()

        # BFS 라서 처음 도달한 순간이 곧 최단거리다
        if r == n - 1 and c == m - 1:
            answer = dist
            break

        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr = r + dr
            nc = c + dc

            if nr < 0 or nr >= n:
                continue
            if nc < 0 or nc >= m:
                continue

            if grid[nr][nc] == '0':
                nb = b            # 빈 칸이면 부순 횟수 그대로
            else:
                nb = b + 1        # 벽이면 하나 부수고 지나간다
                if nb > k:
                    continue      # 더는 못 부순다

            if visited[nr][nc][nb]:
                continue

            visited[nr][nc][nb] = True
            q.append((nr, nc, nb, dist + 1))

print(answer)
