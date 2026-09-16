import sys

input = sys.stdin.readline

BUCKETS = 50021   # 넉넉한 소수


def my_hash(s):
    """문자열 s 를 0 ~ BUCKETS-1 범위의 정수로 바꾼다."""
    h = 0
    for c in s:
        # 자리올림하듯 앞 글자를 31배씩 밀어 올린다 -> 글자 순서까지 반영된다
        h = h * 31 + ord(c)
    return h % BUCKETS


class HashMap:
    def __init__(self):
        # 버킷마다 빈 리스트 하나씩. 여기에 [단어, 횟수] 쌍을 매단다.
        self.table = [[] for _ in range(BUCKETS)]

    def add(self, word):
        """word 의 횟수를 1 늘린다. 없으면 새로 만든다."""
        idx = my_hash(word)
        bucket = self.table[idx]
        # 같은 칸에 매달린 것들만 훑는다. 버킷이 넉넉하면 보통 1~2개뿐이라 사실상 O(1)
        for entry in bucket:
            if entry[0] == word:
                entry[1] += 1
                return
        # 끝까지 없었으면 이 단어는 처음 나온 것
        bucket.append([word, 1])

    def items(self):
        """저장된 모든 [단어, 횟수] 를 하나씩 내놓는다."""
        for bucket in self.table:
            for entry in bucket:
                yield entry


n = int(input())
hm = HashMap()
for _ in range(n):
    hm.add(input().strip())

best_word = None
best_cnt = -1
for word, cnt in hm.items():
    # 횟수가 더 크거나, 횟수가 같은데 사전순으로 앞서면 갱신
    # (첫 번째 단어는 cnt > -1 이 바로 참이라 best_word 가 None 이어도 안전하다)
    if cnt > best_cnt or (cnt == best_cnt and word < best_word):
        best_word = word
        best_cnt = cnt

print(best_word)
