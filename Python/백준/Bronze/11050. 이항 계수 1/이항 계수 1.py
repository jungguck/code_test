n, k = map(int, input().split())

a = 1
b = 1

# n!/(n-k)!
for i in range(n, n-k, -1):
    a *= i  # n, n-1, ..., n-k+1까지 곱셈

# k!
for j in range(1, k+1):
    b *= j  # 1부터 k까지 곱셈

# n!/((n-k)!*k!) 계산
print(a // b)  # 나눗셈 연산
