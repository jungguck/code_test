while True:
    n = input()
    if n == '0':
        break

    for i in range(len(n)//2):
        if n[i] != n[len(n)-1-i]:
            print("no")
            break
    else:
        print("yes")