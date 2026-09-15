import heapq
import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])

    jobs = []
    for i in range(n):
        d = int(data[1 + 2 * i])
        c = int(data[2 + 2 * i])
        jobs.append((d, c))

    # TODO 1: jobs 를 마감일 오름차순으로 정렬한다

    heap = []       # 채택한 작업들의 보상을 담는 최소 힙
    total = 0
    for d, c in jobs:
        # TODO 2: c 를 힙에 넣고 total 에 더한다 (일단 채택)
        # TODO 3: 힙 크기가 d 를 "넘으면" 가장 작은 보상을 빼고 total 에서 뺀다
        pass

    print(total)


main()
