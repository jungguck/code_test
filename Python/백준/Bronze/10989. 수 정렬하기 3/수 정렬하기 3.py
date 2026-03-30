import sys
input = sys.stdin.readline

n = int(input())
count = [0] * 10001

for _ in range(n):
    x = int(input())
    count[x] += 1

for i in range(1, 10001):
    for _ in range(count[i]):
        print(i)