a = list(map(int, input().split()))

if a[1] > a[0]:
    result = "ascending"
elif a[1] < a[0]:
    result = "descending"
    
for i in range(1, 8):
    if a[i] > a[i-1]:
        if result == "descending":  # 내려가다가 올라가면
            result = "mixed"
            break
    elif a[i] < a[i-1]:
        if result == "ascending":   # 올라가다가 내려가면
            result = "mixed"
            break
        result = "descending"  # ← 이게 빠져있었어요!

print(result)