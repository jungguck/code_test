a = []
for i in range(10):
    a.append(int(input()))
    
b = []
cou = 0
for i in range(10):
    remainder = a[i] % 42
    
    if remainder not in b:
        cou += 1
        b.append(remainder) 
        
print(cou)