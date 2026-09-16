import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])

    cnt = [0] * m
    cnt[0] = 1          # P[0] = 0 — 이걸 빼먹으면 1번부터 시작하는 구간을 다 놓친다

    s = 0
    for i in range(2, 2 + n):
        s = (s + int(data[i])) % m      # 누적합을 매번 M으로 접어둔다
        cnt[s] += 1

    # 나머지가 같은 누적합 두 개를 고르면 그 사이 구간은 M의 배수
    total = 0
    for c in cnt:
        total += c * (c - 1) // 2

    print(total)


main()
