n = int(input())
jobs = [tuple(map(int, input().split())) for _ in range(n)]   # (시작, 끝) N개

jobs.sort(key=lambda x: (x[1], x[0]))   # 끝나는 시각 오름차순 (그리디 핵심)

cnt = 0
end = -1                                # 마지막으로 고른 작업의 끝 시각
for s, e in jobs:
    if s >= end:                        # 겹치지 않으면 (끝==시작 은 이어서 OK)
        cnt += 1
        end = e
print(cnt)
