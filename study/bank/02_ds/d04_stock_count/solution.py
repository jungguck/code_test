input()                              # N 은 실제로 쓰지 않으므로 그냥 읽어서 버린다
parts = input().split()

input()                              # M 도 마찬가지
queries = input().split()

# 이름 -> 개수 를 한 번에 세어둔다
stock = {}
for name in parts:
    # 이미 있으면 그 값 +1, 처음 보는 이름이면 0 +1
    stock[name] = stock.get(name, 0) + 1

# 조회는 한 번에 끝난다. 없는 이름은 get 이 0 을 돌려준다
answer = [stock.get(name, 0) for name in queries]

print(*answer)
