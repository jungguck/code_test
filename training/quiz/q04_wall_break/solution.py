import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    grid = [data[3 + i].decode() for i in range(n)]

    # visited[r][c][b] = (r,c) 에 벽을 b번 부순 상태로 와봤는가
    visited = [[[False] * (k + 1) for _ in range(m)] for _ in range(n)]

    # TODO 1: 시작 칸이 벽('1')이면 부순 횟수 1로 시작. 그게 k를 넘으면 -1 출력하고 끝.
    start_b = 0

    q = deque()
    q.append((0, 0, start_b, 1))          # (행, 열, 부순횟수, 지나온 칸 수)
    visited[0][0][start_b] = True

    while q:
        r, c, b, dist = q.popleft()
        # TODO 2: 도착((n-1, m-1))이면 dist 를 출력하고 종료
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr = r + dr
            nc = c + dc
            if not (0 <= nr < n and 0 <= nc < m):
                continue
            # TODO 3: 빈 칸이면 -> b 그대로, 아직 안 가본 상태일 때만 push
            # TODO 4: 벽이면  -> b < k 일 때만 b+1 로 push
            #         (둘 다 push 하는 순간 visited 를 켤 것!)

    print(-1)


main()
