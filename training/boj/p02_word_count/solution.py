import sys

input = sys.stdin.readline

n = int(input())
words = [input().strip() for _ in range(n)]

# 1) dict 로 횟수 세기
cnt = {}
for w in words:
    cnt[w] = cnt.get(w, 0) + 1      # 없으면 0에서 시작, 있으면 +1

# 2) 횟수는 큰 게, 단어는 작은 게 이김
#    -cnt[w] 로 부호를 뒤집으면 "둘 다 작은 게 이김"이 되어 min 한 방에 끝난다
print(min(cnt, key=lambda w: (-cnt[w], w)))
