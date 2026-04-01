isbn = input()
star_idx = 0
total_sum = 0

# 1. 별 위치 찾고, 나머지 합 구하기
for i in range(13):
    if isbn[i] == '*':
        star_idx = i
    else:
        num = int(isbn[i])
        if i % 2 == 0:
            total_sum += num
        else:
            total_sum += num * 3

# 2. 별 자리에 0~9 대입해서 정답 찾기 (이게 j 반복문!)
for j in range(10):
    weight = 1 if star_idx % 2 == 0 else 3
    if (total_sum + j * weight) % 10 == 0:
        print(j)
        break