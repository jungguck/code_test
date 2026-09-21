from collections import deque

n = int(input())

# 1번부터 N번까지 순서대로 큐에 넣는다
cards = deque(range(1, n + 1))

# 카드가 두 장 이상 남아있는 동안 반복
while len(cards) > 1:
    cards.popleft()                 # 맨 위 카드를 버린다
    cards.append(cards.popleft())   # 그 다음 카드를 빼서 맨 아래에 붙인다

print(cards[0])
