# Authored by : gusdn3477
# Co-authored by : -
# Link : http://boj.kr/efd53a96cfd04ca9ab21018162c3084d
from collections import deque

N, M = map(int, input().split())
ans = 0
dic = {}
for i in range(N):
    a = input()
    dic[a] = 1
for i in range(M):
    a = input()
    if a in dic:
        ans += 1
print(ans)
