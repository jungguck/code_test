T = int(input())
 
for test_case in range(1, T + 1):
    n = int(input())
    sequence = [1, 1]
    for i in range(2, n+1):
        k = i//2
        result = 1
        while True:
            satisfied = True
            for j in range(1, k+1):
                a = sequence[i-j] - sequence[i-2*j]
                b = result - sequence[i-j]
                if a == b:
                    satisfied = False
                    break
            if satisfied == True:
                sequence.append(result)
                break
            else:
                result += 1
    print(sequence[n])
