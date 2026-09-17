from itertools import combinations

n, m = map(int, input().split())         # 부품 수, 상한 M
a = list(map(int, input().split()))

best = 0
for x, y, z in combinations(a, 3):       # 서로 다른 3개를 모두 시도
    s = x + y + z
    if s <= m and s > best:              # M 이하이면서 가장 큰 합
        best = s
print(best)
