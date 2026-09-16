import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    grid = [data[2 + i].decode() for i in range(n)]

    visited = [[False] * m for _ in range(n)]
    count = 0       # 구역 개수
    biggest = 0     # 가장 큰 구역의 칸 수

    for sr in range(n):
        for sc in range(m):
            # 먼지도 아니고 이미 본 칸이면 건너뛴다
            if grid[sr][sc] != '1' or visited[sr][sc]:
                continue

            # 여기서부터 새 구역 하나를 통째로 먹어치운다
            count += 1
            visited[sr][sc] = True
            q = deque()
            q.append((sr, sc))
            size = 0

            while q:
                r, c = q.popleft()
                size += 1
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr = r + dr
                    nc = c + dc
                    # 범위 체크를 먼저! 그래야 grid[nr][nc] 접근이 안전하다
                    if 0 <= nr < n and 0 <= nc < m:
                        if not visited[nr][nc] and grid[nr][nc] == '1':
                            visited[nr][nc] = True   # 넣을 때 바로 방문 처리
                            q.append((nr, nc))

            if size > biggest:
                biggest = size

    print(count, biggest)


main()
