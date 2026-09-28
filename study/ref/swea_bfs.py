T = int(input())

for tc in range(1, T + 1):
    n = int(input())
    node = [list(map(int, input().split())) for _ in range(n)]

    # key(부모 노드)와 value(자식 노드)를 저장할 딕셔너리
    grid = {}
    for i in range(n):
        for j in range(n):
            if node[i][j] == 1:
                grid.setdefault(i, []).append(j)

    que = [0]
    visited = []
    while que:
        t = que.pop(0)
        if t not in visited:
            visited.append(t)
        for v in grid.get(t, []):
            if v not in que and v not in visited:
                que.append(v)

    print(f'#{tc}', *visited)
