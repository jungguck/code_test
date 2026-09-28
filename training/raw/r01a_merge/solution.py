import sys
input = sys.stdin.readline

n, m = map(int, input().split())
left = list(map(int, input().split()))
right = list(map(int, input().split()))

result = []
i = 0   # left 에서 볼 위치
j = 0   # right 에서 볼 위치

# 양쪽 다 남아있는 동안: 맨 앞 두 개를 비교해 큰 쪽을 가져온다 (내림차순이니까)
while i < len(left) and j < len(right):
    if left[i] >= right[j]:
        result.append(left[i])
        i += 1
    else:
        result.append(right[j])
        j += 1

# 한쪽이 바닥나면 다른 쪽에 남은 건 이미 정렬돼 있으니 그대로 붙인다
while i < len(left):
    result.append(left[i])
    i += 1
while j < len(right):
    result.append(right[j])
    j += 1

print(*result)
