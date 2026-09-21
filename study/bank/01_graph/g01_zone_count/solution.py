from collections import deque

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]

# 상, 하, 좌, 우 네 방향. dx[i], dy[i] 를 짝지어 쓴다.
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

count = 0

for i in range(n):
    for j in range(m):
        # 짐이 있고(1) 아직 방문 안 한 칸을 만나면, 새 덩어리를 하나 발견한 것
        if board[i][j] == 1:
            count += 1

            # 여기서부터 붙어있는 칸을 전부 찾아서 0으로 지운다.
            # 지워두면 나중에 다시 세지 않는다 (= 방문 표시)
            queue = deque()
            queue.append((i, j))
            board[i][j] = 0

            while queue:
                x, y = queue.popleft()
                for d in range(4):
                    nx = x + dx[d]
                    ny = y + dy[d]
                    if nx < 0 or nx >= n or ny < 0 or ny >= m:
                        continue            # 판 밖으로 나가면 무시
                    if board[nx][ny] == 0:
                        continue            # 빈 칸이거나 이미 지운 칸
                    board[nx][ny] = 0       # 지우고
                    queue.append((nx, ny))  # 여기서도 이어서 퍼진다

print(count)
