import sys

input = sys.stdin.readline
sys.setrecursionlimit(10 ** 6)


def merge(left, right):
    """이미 내림차순으로 정렬된 두 리스트를 합쳐서 하나의 내림차순 리스트로."""
    result = []
    i = 0   # left 에서 볼 위치
    j = 0   # right 에서 볼 위치

    # TODO 1: 양쪽 다 남아있는 동안, 앞쪽 두 개를 비교해서 큰 쪽을 result 에 붙이고
    #         그쪽 인덱스를 1 증가시킨다

    # TODO 2: 한쪽이 먼저 바닥나면, 다른 쪽에 남은 것들을 전부 뒤에 붙인다

    return result


def merge_sort(arr):
    """arr 을 내림차순으로 정렬한 새 리스트를 반환."""
    # TODO 3: 길이가 1 이하면 이미 정렬된 것이므로 그대로 반환 (종료조건)

    # TODO 4: 가운데를 기준으로 반으로 쪼개서 각각 merge_sort 를 재귀 호출하고,
    #         그 둘을 merge 해서 반환
    raise NotImplementedError


n = int(input())
nums = list(map(int, input().split()))

print(*merge_sort(nums))
