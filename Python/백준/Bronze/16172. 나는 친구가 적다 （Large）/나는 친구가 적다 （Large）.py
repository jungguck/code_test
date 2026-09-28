import sys
input = sys.stdin.readline
S = input().rstrip()
K = input().rstrip()

for i in range(10):
    S = S.replace(str(i), '')

print(1 if K in S else 0)