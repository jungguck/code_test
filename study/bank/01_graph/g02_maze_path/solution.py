from collections import deque

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# dist[i][j] = 출발점에서 (i,j) 까지 지나온 칸 수. 0 이면 아직 안 가본 칸
dist = [[0] * m for _ in range(n)]

queue = deque()
queue.append((0, 0))
dist[0][0] = 1          # 출발 칸도 세므로 1 부터 시작

while queue:
    x, y = queue.popleft()

    for d in range(4):
        nx = x + dx[d]
        ny = y + dy[d]
        if nx < 0 or nx >= n or ny < 0 or ny >= m:
            continue                    # 판 밖
        if board[nx][ny] == 0:
            continue                    # 벽
        if dist[nx][ny] != 0:
            continue                    # 이미 더 짧은 길로 와본 칸

        dist[nx][ny] = dist[x][y] + 1   # 한 칸 더 간 것
        queue.append((nx, ny))

# 도착 칸이 0 이면 끝내 못 갔다는 뜻
print(dist[n - 1][m - 1] if dist[n - 1][m - 1] != 0 else -1)
