import sys

input = sys.stdin.readline
sys.setrecursionlimit(10 ** 6)


def merge(left, right):
    """이미 내림차순으로 정렬된 두 리스트를 합쳐서 하나의 내림차순 리스트로."""
    result = []
    i = 0   # left 에서 볼 위치
    j = 0   # right 에서 볼 위치

    # 양쪽 다 남아있는 동안: 앞쪽 두 개를 비교해 "큰 쪽"을 가져온다 (내림차순이니까)
    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 한쪽이 바닥나면 다른 쪽에 남은 건 이미 정렬되어 있으니 그대로 붙인다
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort(arr):
    """arr 을 내림차순으로 정렬한 새 리스트를 반환."""
    # 종료조건: 원소가 0개나 1개면 이미 정렬된 상태다
    if len(arr) <= 1:
        return arr

    # 반으로 쪼개서 각각 정렬한 뒤(분할), 둘을 합친다(정복)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


n = int(input())
nums = list(map(int, input().split()))

print(*merge_sort(nums))
