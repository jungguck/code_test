import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])

    cnt = [0] * m
    # TODO 1: P[0] = 0 도 누적합 하나다. cnt 를 어떻게 초기화해야 할까?

    s = 0
    for i in range(2, 2 + n):
        # TODO 2: s 에 값을 더하고 m 으로 나눈 나머지만 남긴 뒤, 그 나머지의 개수를 센다
        pass

    total = 0
    # TODO 3: 각 나머지 개수 c 마다 두 개를 고르는 경우의 수를 더한다
    print(total)


main()
