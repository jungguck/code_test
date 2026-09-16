import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])

    # prev2 = dp[i-2], prev1 = dp[i-1]
    # 배열을 안 만들고 변수 두 개로만 굴린다 -> O(1) 메모리
    prev2 = 0
    prev1 = 0

    for i in range(1, 1 + n):
        x = int(data[i])
        # 오늘 쉰다: prev1 그대로 / 오늘 일한다: 어제는 쉬었어야 하므로 prev2 + x
        cur = prev1 if prev1 > prev2 + x else prev2 + x
        prev2 = prev1
        prev1 = cur

    print(prev1)


main()
