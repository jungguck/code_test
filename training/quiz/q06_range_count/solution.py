import sys
from bisect import bisect_left, bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])

    a = sorted(map(int, data[2:2 + n]))     # 정렬은 딱 한 번

    out = []
    p = 2 + n
    for _ in range(q):
        lo = int(data[p])
        hi = int(data[p + 1])
        p += 2
        # bisect_left(lo)  = lo 이상인 첫 위치
        # bisect_right(hi) = hi 초과인 첫 위치
        out.append(bisect_right(a, hi) - bisect_left(a, lo))

    # print 를 20만 번 부르지 않고 한 번에 내보낸다
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
