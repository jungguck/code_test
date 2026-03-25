n = int(input())

for _ in range(n):
    s = input()
    count = 0

    for ch in s:
        if ch == 'U':
            count += 1
        else:
            break

    print(count)