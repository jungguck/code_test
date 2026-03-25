n = int(input())
w = int(input())

point = 10 * n

if n >= 3:
    point += 20

if n == 5:
    point += 50

if w > 1000:
    point -= 15

print(max(point,0))