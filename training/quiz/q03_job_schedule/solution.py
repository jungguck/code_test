import sys
import heapq

input = sys.stdin.readline

n = int(input())

jobs = []
for _ in range(n):
    d, c = map(int, input().split())    # 마감일, 보상
    jobs.append((d, c))

jobs.sort()      # 마감일 오름차순 (튜플은 앞 원소부터 비교한다)

heap = []        # 지금까지 채택한 작업들의 보상 (최소 힙)
total = 0

for d, c in jobs:
    # ① 일단 채택한다
    heapq.heappush(heap, c)
    total += c

    # ② d일까지는 d개만 할 수 있다. 넘쳤으면 제일 싼 걸 포기한다
    if len(heap) > d:
        smallest = heapq.heappop(heap)
        total -= smallest

print(total)
