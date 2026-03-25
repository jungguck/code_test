n = int(input())
trophies = []
for _ in range(n):
    trophies.append(int(input()))

# 2. 개수 세는 로직 정의
def count_visible(lst):
    count = 0
    max_h = 0
    for h in lst:
        if h > max_h:
            count += 1
            max_h = h
    return count

# 3. 출력
print(count_visible(trophies))         # 왼쪽
print(count_visible(trophies[::-1]))   # 오른쪽 (리스트 뒤집기)