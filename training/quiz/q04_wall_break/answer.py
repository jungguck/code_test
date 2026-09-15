import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    grid = [data[3 + i].decode() for i in range(n)]

    # visited[r][c] = 그 칸에 "부순 횟수 b" 로 와봤는지 (b = 0..k)
    visited = [[[False] * (k + 1) for _ in range(m)] for _ in range(n)]

    # 시작 칸이 벽이면 그것부터 부수고 시작한다
    start_b = 1 if grid[0][0] == '1' else 0
    if start_b > k:
        print(-1)
        return

    q = deque()
    q.append((0, 0, start_b, 1))          # (행, 열, 부순횟수, 지나온 칸 수)
    visited[0][0][start_b] = True

    while q:
        r, c, b, dist = q.popleft()
        if r == n - 1 and c == m - 1:     # BFS 라서 처음 도달한 순간이 최단
            print(dist)
            return
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr = r + dr
            nc = c + dc
            if not (0 <= nr < n and 0 <= nc < m):
                continue
            if grid[nr][nc] == '0':
                if not visited[nr][nc][b]:
                    visited[nr][nc][b] = True     # push 할 때 바로 켠다
                    q.append((nr, nc, b, dist + 1))
            else:
                if b < k and not visited[nr][nc][b + 1]:
                    visited[nr][nc][b + 1] = True
                    q.append((nr, nc, b + 1, dist + 1))

    print(-1)


main()
