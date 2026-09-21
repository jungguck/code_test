from collections import deque

n, m = map(int, input().split())

# adj[i] = i번이 아는 사람들의 번호 목록 (인접 리스트)
# 0번은 안 쓰고 1~N 번만 쓰려고 n+1 개를 만든다
adj = [[] for _ in range(n + 1)]

for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)    # 아는 사이는 양방향이므로
    adj[b].append(a)    # 양쪽에 다 넣어준다

# day[i] = i번이 소문을 듣는 날짜. -1 이면 아직 못 들음
day = [-1] * (n + 1)
day[1] = 0                  # 1번은 0일차에 이미 알고 있다

queue = deque()
queue.append(1)

while queue:
    cur = queue.popleft()
    for nxt in adj[cur]:
        if day[nxt] == -1:              # 아직 못 들은 사람에게만
            day[nxt] = day[cur] + 1     # 하루 뒤에 듣는다
            queue.append(nxt)

# 1번을 빼고, 들은 사람(-1 이 아닌 사람)만 센다
heard = [day[i] for i in range(2, n + 1) if day[i] != -1]

if not heard:
    print(0, 0)
else:
    print(len(heard), max(heard))
