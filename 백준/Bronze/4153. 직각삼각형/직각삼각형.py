while True:
    a, b, c = map(int, input().split())

    if a == 0 and b == 0 and c == 0:
        break

    if a >= b and a >= c:
        max = a
        x = b
        y = c
    elif b >= a and b >= c:
        max = b
        x = a
        y = c
    else:
        max = c
        x = a
        y = b

    if x*x + y*y == max*max:
        print("right")
    else:
        print("wrong")