res = 0

for _ in range(int(input())):
    s = input()

    if "CD" not in s:
        res += 1
print(res)