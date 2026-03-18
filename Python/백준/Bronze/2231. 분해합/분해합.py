n = int(input())

def digist_sum(x):
    total = 0
    
    while x>0:
        total += x %10
        x = x // 10
        
    return total
        

for x in range(1,n+1):
    if x+digist_sum(x) == n:
        print(x)
        break
else:
    print(0)