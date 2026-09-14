import sys

input = sys.stdin.readline

OPEN = "([{"
CLOSE = ")]}"


class Stack:
    """고정 크기 배열 + top 인덱스로 만든 스택."""

    def __init__(self, capacity):
        self.data = [None] * capacity   # 미리 자리를 다 잡아둔다
        self.top = -1                   # -1 은 "비어있음"

    def is_empty(self):
        # TODO 1: 비어있는지 True/False 로 반환
        raise NotImplementedError

    def push(self, value):
        # TODO 2: top 을 1 올리고, 그 자리에 value 를 넣는다
        raise NotImplementedError

    def pop(self):
        # TODO 3: 현재 top 자리의 값을 읽어두고, top 을 1 내린 뒤, 읽어둔 값을 반환
        #         (비어있으면 None 을 반환하게 해두면 아래에서 쓰기 편하다)
        raise NotImplementedError


t = int(input())
for _ in range(t):
    s = input().strip()
    stack = Stack(len(s))
    ok = True

    for ch in s:
        if ch in OPEN:
            # TODO 4: 여는 괄호면 스택에 쌓는다
            pass
        else:
            # TODO 5: 닫는 괄호면 스택에서 하나 꺼내서,
            #         그게 이 닫는 괄호의 짝(OPEN[CLOSE.index(ch)])이 맞는지 확인.
            #         비어있거나 짝이 틀리면 ok = False 하고 break
            pass

    # TODO 6: ok 이고 스택이 비어있으면 YES, 아니면 NO 출력
    print("NO")
