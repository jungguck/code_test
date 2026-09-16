from collections import deque

n, m = map(int, input().split())

grid = []
for _ in range(n):
    grid.append(input())     # input() 은 줄 끝 개행을 알아서 떼어준다

visited = [[False] * m for _ in range(n)]

count = 0        # 구역 개수
biggest = 0      # 가장 큰 구역의 칸 수

for sr in range(n):
    for sc in range(m):
        # 먼지가 아니거나 이미 본 칸이면 넘어간다
        if grid[sr][sc] != '1':
            continue
        if visited[sr][sc]:
            continue

        # 여기서부터 새 구역 하나를 통째로 먹어치운다
        count += 1

        q = deque()
        q.append((sr, sc))
        visited[sr][sc] = True
        size = 0

        while q:
            r, c = q.popleft()
            size += 1

            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr = r + dr
                nc = c + dc

                # 갈 수 없는 이유를 하나씩 걸러낸다
                if nr < 0 or nr >= n:
                    continue          # 위아래로 격자 밖
                if nc < 0 or nc >= m:
                    continue          # 좌우로 격자 밖
                if visited[nr][nc]:
                    continue          # 이미 가본 칸
                if grid[nr][nc] != '1':
                    continue          # 먼지가 아님

                visited[nr][nc] = True   # 큐에 "넣을 때" 바로 방문 처리!
                q.append((nr, nc))

        if size > biggest:
            biggest = size

print(count, biggest)
