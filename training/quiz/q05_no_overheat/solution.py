n = int(input())
a = list(map(int, input().split()))

# dp[i] = i일째까지 봤을 때 얻을 수 있는 최대 성과
dp = [0] * n
dp[0] = a[0]
if n > 1:
    dp[1] = max(a[0], a[1])              # 첫 이틀은 붙여 못 하니 더 큰 하루

for i in range(2, n):
    # 오늘 쉰다: dp[i-1]  /  오늘 일한다: dp[i-2] + a[i]  (어제는 쉬었어야)
    dp[i] = max(dp[i - 1], dp[i - 2] + a[i])

print(dp[n - 1])
