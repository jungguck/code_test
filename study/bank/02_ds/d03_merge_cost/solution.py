import heapq

n = int(input())

# heap 에 넣어두면 "가장 작은 값" 을 언제든 O(log N) 에 꺼낼 수 있다
heap = []
for _ in range(n):
    heapq.heappush(heap, int(input()))

total = 0

# 묶음이 두 개 이상 남아있는 동안 계속 합친다
while len(heap) > 1:
    a = heapq.heappop(heap)     # 가장 가벼운 것
    b = heapq.heappop(heap)     # 그 다음으로 가벼운 것

    cost = a + b
    total += cost               # 합치는 비용을 누적

    heapq.heappush(heap, cost)  # 합쳐진 묶음을 다시 넣는다

print(total)
