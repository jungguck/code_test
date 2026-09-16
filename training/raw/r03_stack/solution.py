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
        return self.top == -1

    def push(self, value):
        self.top += 1               # 빈 자리로 한 칸 올라가서
        self.data[self.top] = value # 거기에 덮어쓴다

    def pop(self):
        if self.top == -1:
            return None             # 비었으면 None (호출한 쪽에서 판단하기 편하게)
        value = self.data[self.top] # 먼저 읽어두고
        self.top -= 1               # top 만 한 칸 내린다
        return value                # 지울 필요 없다. 다음 push 가 덮어쓸 자리니까


t = int(input())
for _ in range(t):
    s = input().strip()
    stack = Stack(len(s))
    ok = True

    for ch in s:
        if ch in OPEN:
            stack.push(ch)                  # 여는 괄호는 쌓아둔다
        else:
            got = stack.pop()               # 닫는 괄호가 오면 가장 최근 것을 꺼낸다
            # CLOSE 에서 ch 의 위치를 찾아 OPEN 의 같은 위치를 보면 짝이 나온다
            if got is None or got != OPEN[CLOSE.index(ch)]:
                ok = False                  # 닫을 게 없거나 종류가 다르다
                break

    # 다 돌고도 스택이 비어있어야 진짜 YES (안 닫힌 게 남아있으면 NO)
    print("YES" if ok and stack.is_empty() else "NO")
