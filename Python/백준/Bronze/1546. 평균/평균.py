n = int(input())
scores = list(map(int, input().split()))

# 네가 하던 방식처럼 max 직접 찾기
max_val = scores[0]

for s in scores:
    if s > max_val:
        max_val = s

# 평균 계산 (네 공식 유지)
average = 0
for s in scores:
    average += (s / max_val) * 100

average = average / n

print(average)