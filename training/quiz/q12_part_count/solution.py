from collections import Counter

n = int(input())
c = Counter(input() for _ in range(n))   # 이름별 등장 횟수 세기

# 가장 많이 나온 것, 동률이면 사전순 앞쪽
name = min(c, key=lambda x: (-c[x], x))
print(name, c[name])
