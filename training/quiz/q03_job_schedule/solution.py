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

    jobs.sort()                     # 마감일 오름차순 (같으면 보상순, 상관없음)

    heap = []                       # 지금까지 채택한 작업들의 보상 (최소 힙)
    total = 0
    for d, c in jobs:
        heapq.heappush(heap, c)     # 일단 채택하고
        total += c
        if len(heap) > d:           # d일까지 d개 초과 -> 칸이 모자람
            total -= heapq.heappop(heap)   # 제일 싼 걸 포기

    print(total)


main()
