import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = int(data[1])
    a = list(map(int, data[2:2 + n]))

    left = 0
    total = 0
    best = n + 1          # 있을 수 없는 큰 값 = "아직 못 찾음"

    for right in range(n):
        total += a[right]                 # 창을 오른쪽으로 한 칸 늘린다

        # 조건을 만족하는 동안 왼쪽을 계속 당겨서 더 짧은 답을 찾는다.
        # left 는 절대 뒤로 안 가므로 전체 이동 횟수는 N번 -> O(N)
        while total >= s:
            if right - left + 1 < best:
                best = right - left + 1
            total -= a[left]
            left += 1

    print(best if best <= n else 0)


main()
