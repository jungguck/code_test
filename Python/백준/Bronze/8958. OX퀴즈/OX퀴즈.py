n = int(input())
for i in range(n):
    cout = 0
    total = 0
    a = input()
    for x in a:
        if x == 'O':
            cout += 1
            total += cout
        elif x == 'X':
            cout = 0
    print(total)