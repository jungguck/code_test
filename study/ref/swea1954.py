T = int(input())

# 우, 하, 좌, 상 (시계 방향 순서)
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

for test_case in range(1, T + 1):
    N = int(input())
    
    # 0으로 채워진 N x N 2차원 리스트 생성
    arr = [[0] * N for _ in range(N)]
    
    r, c = 0, 0      # 시작 위치 (0, 0)
    direction = 0    # 초기 방향: 우측 (dr[0], dc[0])
    
    for num in range(1, N * N + 1):
        arr[r][c] = num
        
        # 다음 이동할 위치 미리 계산
        nr = r + dr[direction]
        nc = c + dc[direction]
        
        # 범위를 벗어나거나 이미 숫자가 채워져 있다면 방향 전환
        if not (0 <= nr < N and 0 <= nc < N) or arr[nr][nc] != 0:
            direction = (direction + 1) % 4  # 0 -> 1 -> 2 -> 3 -> 0 순환
            nr = r + dr[direction]
            nc = c + dc[direction]
            
        r, c = nr, nc

    # 출력 양식 맞추기
    print(f"#{test_case}")
    for row in arr:
        print(*row)
