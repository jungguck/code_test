import sys

data = sys.stdin.read().split()

n = int(data[0])
b = int(data[1])
ds = data[2:2 + n]

empty = 0
for x in ds:
    d = int(x)
    # TODO 1: b 에 d 를 더하고, 0 ~ 100 범위로 잘라라 (clamp)
    # TODO 2: 자른 뒤의 b 가 0이면 empty 를 1 늘려라
    pass

print(b, empty)
