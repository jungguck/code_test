import sys

data = sys.stdin.read().split()

n = int(data[0])
b = int(data[1])
ds = data[2:2 + n]

empty = 0
for x in ds:
    b += int(x)
    # 위아래를 한 번에 자른다: 0 밑으로도, 100 위로도 못 간다
    if b < 0:
        b = 0
    elif b > 100:
        b = 100
    # 자른 "뒤" 값이 0일 때만 방전으로 센다
    if b == 0:
        empty += 1

print(b, empty)
