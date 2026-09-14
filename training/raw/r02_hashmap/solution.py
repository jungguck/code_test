import sys

input = sys.stdin.readline

BUCKETS = 50021   # 넉넉한 소수


def my_hash(s):
    """문자열 s 를 0 ~ BUCKETS-1 범위의 정수로 바꾼다."""
    h = 0
    # TODO 1: 각 글자마다  h = h * 31 + ord(c)
    #         마지막에 h % BUCKETS 를 반환
    return h % BUCKETS


class HashMap:
    def __init__(self):
        # 버킷마다 빈 리스트 하나씩. 여기에 [단어, 횟수] 쌍을 매단다.
        self.table = [[] for _ in range(BUCKETS)]

    def add(self, word):
        """word 의 횟수를 1 늘린다. 없으면 새로 만든다."""
        idx = my_hash(word)
        bucket = self.table[idx]
        # TODO 2: bucket 안을 훑어서 같은 단어가 있으면 그 횟수를 +1 하고 끝낸다
        # TODO 3: 끝까지 없었으면 bucket 에 [word, 1] 을 새로 추가한다
        raise NotImplementedError

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
    # TODO 4: 횟수가 더 크거나 / 횟수가 같은데 사전순으로 앞서면 best 갱신
    pass

print(best_word)
