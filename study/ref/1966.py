# Authored by : gusdn3477
# Co-authored by : -
# Link : http://boj.kr/74b1e7adb56b425aa6644b3d2ea726e0
from collections import deque

T = int(input())
for i in range(T):
    queue = deque()
    queue2 = deque()
    ct = 1
    N,M = map(int, input().split())
    arr = list(map(int, input().split()))
    for j in range(len(arr)):
        queue.append(arr[j])
        queue2.append(j)
    while True:
        if queue[0] == max(queue):
            if queue2[0] == M:
                print(ct)
                break
            else:
                queue.popleft()
                queue2.popleft()
                ct += 1
        else:
            queue.rotate(-1)
            queue2.rotate(-1)
