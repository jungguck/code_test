n = int(input())

num = list(map(int,input().split()))

min = num[0]
max = num[0]
for i in range(n):
    a = num[i]
    if num[i] < min:
        min = a
    if num[i] > max:
        max = a
        
print(min, max)