
import sys
input = sys.stdin.readline

n = int(input())
nums = list(map(int,input().split()))

nums.sort(reverse=True)

print(*nums)