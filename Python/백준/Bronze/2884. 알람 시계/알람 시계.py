a, b = map(int, input().split())

if b >= 45:
    b -= 45
else:
    b += 15
    a -= 1
    if a < 0:
        a = 23

print(a, b)