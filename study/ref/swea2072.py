n = int(input())

for i in range(1, n + 1):
    numbers = list(map(int, input().split()))
    odd_sum = 0

    for num in numbers:
        if num % 2 == 1:
            odd_sum += num

    print(f"#{i} {odd_sum}")
