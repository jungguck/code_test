from collections import deque

n, m = map(int, input().split())        # 상자 개수, 명령 개수
a = deque(map(int, input().split()))    # 벨트 위 상자들

for _ in range(m):
    cmd, k = input().split()            # 예: "R 2"  (문자 하나 + 숫자)
    k = int(k) % n                      # n 이상 돌면 제자리 -> 나머지만큼만
    if cmd == "L":
        a.rotate(-k)                    # 왼쪽 회전은 음수
    else:
        a.rotate(k)                     # 오른쪽 회전은 양수

print(*a)                               # 리스트를 공백으로 풀어서 출력
