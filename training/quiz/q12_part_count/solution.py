from collections import Counter

n = int(input())
names = [input() for _ in range(n)]

cnt = Counter(names)                        # 이름별 등장 횟수 세기

best = max(cnt.values())                    # 가장 많이 나온 횟수
winners = [name for name in cnt if cnt[name] == best]   # 그 횟수인 이름들
print(min(winners), best)                   # 사전순 가장 앞선 이름 + 그 횟수
