a = int(input())
b = int(input())
c = int(input())

d = a * b * c

for i in range(10):
    print(str(d).count(str(i)))