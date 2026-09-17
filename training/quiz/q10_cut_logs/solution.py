n, m = map(int, input().split())         # 통나무 수, 필요한 길이 합
a = list(map(int, input().split()))      # 입력은 두 줄뿐이라 그냥 input() 이면 충분

lo, hi = 0, max(a)                       # 절단기 높이 후보 범위
ans = 0
while lo <= hi:
    mid = (lo + hi) // 2                  # 높이 mid 로 잘라본다
    total = sum(x - mid for x in a if x > mid)   # mid 초과분의 합
    if total >= m:                       # 충분히 얻으면 더 높여본다
        ans = mid
        lo = mid + 1
    else:                                # 모자라면 낮춘다
        hi = mid - 1
print(ans)
