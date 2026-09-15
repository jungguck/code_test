import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = int(data[1])
    a = list(map(int, data[2:2 + n]))

    left = 0
    total = 0
    best = n + 1          # "아직 못 찾음" 을 뜻하는 값

    for right in range(n):
        # TODO 1: a[right] 를 total 에 더해 창을 오른쪽으로 늘린다
        # TODO 2: total 이 s 이상인 "동안" (while!)
        #           - best 를 (right - left + 1) 과 비교해 갱신
        #           - total 에서 a[left] 를 빼고 left 를 한 칸 전진
        pass

    # TODO 3: 한 번도 못 찾았으면 0, 찾았으면 best 를 출력
    print(best)


main()
