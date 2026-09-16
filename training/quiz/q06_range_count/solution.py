import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))

a.sort()      # 정렬은 딱 한 번만. 이후 질의는 이분탐색으로 처리한다

answers = []

for _ in range(q):
    lo, hi = map(int, input().split())

    start = bisect_left(a, lo)     # lo 이상인 첫 위치
    end = bisect_right(a, hi)      # hi 초과인 첫 위치

    answers.append(end - start)    # 그 사이에 있는 개수

# print 를 질의마다 부르면 느리다. 한 번에 모아서 출력한다
print("\n".join(map(str, answers)))
