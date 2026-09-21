n, s = map(int, input().split())
nums = list(map(int, input().split()))

best = n + 1      # 있을 수 없는 큰 값으로 시작 (아직 못 찾음 표시)
left = 0          # 구간의 왼쪽 끝
total = 0         # 지금 구간(left ~ right)의 합

for right in range(n):
    total += nums[right]        # 오른쪽을 한 칸 넓히고 그 값을 더한다

    # 합이 S 이상이면, 왼쪽을 줄여가며 더 짧게 만들 수 있는지 본다
    while total >= s:
        length = right - left + 1
        if length < best:
            best = length

        total -= nums[left]     # 왼쪽 값을 빼고
        left += 1               # 왼쪽 끝을 한 칸 오른쪽으로

# best 가 그대로면 S 이상인 구간이 한 번도 없었다는 뜻
print(best if best <= n else 0)
