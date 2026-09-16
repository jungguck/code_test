import sys

input = sys.stdin.readline

n, s = map(int, input().split())
a = list(map(int, input().split()))

left = 0            # 창의 왼쪽 끝
total = 0           # 지금 창 안의 합
best = n + 1        # 있을 수 없는 값 = "아직 답을 못 찾음"

for right in range(n):
    total += a[right]          # 창을 오른쪽으로 한 칸 늘린다

    # 조건을 만족하는 동안 왼쪽을 계속 당겨서 더 짧은 답을 찾는다
    while total >= s:
        length = right - left + 1

        if length < best:
            best = length

        total -= a[left]       # 왼쪽 한 칸을 창 밖으로 뺀다
        left += 1

# left 는 절대 뒤로 안 가므로 전체 이동 횟수는 n번 -> O(N)

if best <= n:
    print(best)
else:
    print(0)       # 한 번도 조건을 만족한 적이 없다
