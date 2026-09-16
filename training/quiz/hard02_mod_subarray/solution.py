n, m = map(int, input().split())
a = list(map(int, input().split()))

cnt = [0] * m      # cnt[r] = 나머지가 r 인 누적합의 개수
cnt[0] = 1         # P[0] = 0 도 누적합 하나다. 이걸 빼먹는 게 최다 실수

s = 0
for x in a:
    s = (s + x) % m     # 누적합을 매번 m 으로 접어둔다
    cnt[s] += 1

# 나머지가 같은 누적합 두 개를 고르면 그 사이 구간은 항상 m의 배수
total = 0
for c in cnt:
    pairs = c * (c - 1) // 2     # c개 중 2개를 고르는 경우의 수
    total += pairs

print(total)
