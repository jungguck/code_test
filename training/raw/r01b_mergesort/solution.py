import sys
input = sys.stdin.readline
sys.setrecursionlimit(10 ** 6)

def merge(left, right):
    """R01a 에서 만든 것 — 이미 내림차순인 두 리스트를 합친다."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] >= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result

def merge_sort(arr):
    """arr 을 내림차순으로 정렬한 새 리스트를 반환. 채워야 할 네 줄."""
    if len(arr) <= 1:               # 한 장이면 이미 정렬된 것
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # 왼쪽 절반을 정렬해서 받는다 (믿고 받는다)
    right = merge_sort(arr[mid:])   # 오른쪽 절반도
    return merge(left, right)       # 둘을 합친다

n = int(input())
nums = list(map(int, input().split()))

print(*merge_sort(nums))
