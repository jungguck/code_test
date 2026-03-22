n, m = map(int, input().split())
a = list(map(int, input().split()))

ans = 0
for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1, n):
            total = a[i] + a[j] + a[k]
            if total <= m:
                ans = max(ans, total)

print(ans)