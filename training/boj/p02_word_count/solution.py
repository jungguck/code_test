from collections import Counter

n = int(input())
words = [input() for _ in range(n)]

cnt = Counter(words)                       # 단어별 등장 횟수 세기

best = max(cnt.values())                   # 가장 많이 나온 횟수
winners = [w for w in cnt if cnt[w] == best]   # 그 횟수인 단어들
print(min(winners))                        # 그 중 사전순으로 가장 앞선 것
