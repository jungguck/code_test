import sys
input = sys.stdin.readline
s = input().rstrip()

for ch in "abcdefghijklmnopqrstuvwxyz":
    print(s.find(ch), end=" ")