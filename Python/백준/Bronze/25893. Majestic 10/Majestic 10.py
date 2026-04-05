import sys

# 테스트 케이스 개수 입력
n = int(input())

for i in range(n):
    line = sys.stdin.readline().split()
    if not line: break # 빈 줄 예외 처리
    
    nums = list(map(int, line))
    
    # 10 이상인 숫자의 개수 카운트
    count = sum(1 for x in nums if x >= 10)
    
    # 1. 원본 숫자들 출력
    print(f"{nums[0]} {nums[1]} {nums[2]}")
    
    # 2. 개수에 따른 정확한 단어 출력
    if count == 0:
        print("zilch")
    elif count == 1:
        print("double")
    elif count == 2:
        print("double-double")
    elif count == 3:
        print("triple-double")
   
    print()