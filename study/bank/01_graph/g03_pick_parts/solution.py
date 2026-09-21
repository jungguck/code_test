n, k, m = map(int, input().split())
weight = list(map(int, input().split()))

best = -1     # 아직 담을 수 있는 경우를 못 찾음


def pick(start, chosen, total):
    """start 번 부품부터 살펴보며 고른다.
       chosen = 지금까지 고른 개수, total = 지금까지의 무게 합"""
    global best

    if total > m:
        return                      # 이미 넘었다. 더 담아봐야 소용없으니 여기서 끊는다

    if chosen == k:
        best = max(best, total)     # K개를 다 골랐다. 후보로 기록
        return

    for i in range(start, n):
        # i번 부품을 고르고, 그 다음 부품부터 이어서 고른다.
        # i+1 로 넘기기 때문에 같은 부품을 두 번 고르지 않는다.
        pick(i + 1, chosen + 1, total + weight[i])


pick(0, 0, 0)
print(best)
