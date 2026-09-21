n = int(input())
nums = list(map(int, input().split()))

answer = [-1] * n     # 기본값은 -1 (못 찾은 상태)
stack = []            # 아직 답을 못 찾은 원소들의 "위치(인덱스)" 를 쌓아둔다

for i in range(n):
    # 스택 맨 위에 있는 수가 지금 들어온 수보다 작다면,
    # 그 수가 기다리던 "다음 큰 수" 가 바로 지금 이 수다.
    while stack and nums[stack[-1]] < nums[i]:
        answer[stack.pop()] = nums[i]

    # 나는 아직 내 답을 모른다. 뒤에 더 큰 수가 나오길 기다리며 쌓인다.
    stack.append(i)

# 끝까지 스택에 남은 것들은 더 큰 수를 못 만난 것 → -1 그대로 둔다

print(*answer)
