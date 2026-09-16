import sys

input = sys.stdin.readline     # 평소 쓰던 input() 과 사용법은 똑같다. 그냥 더 빠른 버전

n, b = map(int, input().split())    # 첫 줄: 동작 횟수, 시작 배터리
ds = list(map(int, input().split()))   # 둘째 줄: 변화량 N개

empty = 0

for d in ds:
    b += d

    # 배터리는 0 ~ 100 을 벗어날 수 없다. 벗어나면 잘라준다
    if b < 0:
        b = 0
    elif b > 100:
        b = 100

    # 자른 "뒤" 값이 0일 때만 방전으로 센다
    if b == 0:
        empty += 1

print(b, empty)
