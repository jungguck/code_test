n = int(input())
a = list(map(int, input().split()))

prev2 = 0     # 그저께까지의 최선  (dp[i-2])
prev1 = 0     # 어제까지의 최선    (dp[i-1])

for x in a:
    # 오늘 할 수 있는 선택은 두 가지뿐이다
    rest = prev1          # ① 오늘 쉰다  -> 어제까지의 최선 그대로
    work = prev2 + x      # ② 오늘 일한다 -> 어제는 쉬었어야 하니까
                          #                그저께까지의 최선 + 오늘 성과

    cur = max(rest, work)  # 둘 중 큰 쪽이 "오늘까지의 최선"

    # 하루 밀기: 어제가 그저께가 되고, 오늘이 어제가 된다
    prev2 = prev1
    prev1 = cur

print(prev1)
