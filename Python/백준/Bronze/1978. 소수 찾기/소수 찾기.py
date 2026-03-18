n = int(input())
cout = 0

a = list(map(int,input().split()))

for i in range(n):
    num = a[i]
    is_prime = True
    if num == 1:
        is_prime = False
    
    for j in range(2, num):
    
        if num % j == 0:
            is_prime = False
            
    if is_prime:
        cout += 1
print(cout)