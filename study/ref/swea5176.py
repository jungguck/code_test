T = int(input())
for test_case in range(1, T + 1):
    N = int(input())
    tree = [0] * (N + 1)
    current_val = 1

    # 비재귀(반복문) 방식의 중위 순회를 위한 스택
    stack = []
    curr = 1

    while curr <= N or stack:
        # 왼쪽 자식 노드로 이동 가능할 때까지 스택에 담고 이동
        while curr <= N:
            stack.append(curr)
            curr *= 2

        # 더 이상 왼쪽으로 갈 수 없으면 스택에서 꺼내어 값 할당
        curr = stack.pop()
        tree[curr] = current_val
        current_val += 1

        # 오른쪽 자식 노드로 이동
        curr = curr * 2 + 1

    print(f"#{test_case} {tree[1]} {tree[N // 2]}")
