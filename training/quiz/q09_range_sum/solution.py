import sys
input = sys.stdin.readline               # 질의가 많을 수 있어 빠른 입력 사용

n, q = map(int, input().split())
a = list(map(int, input().split()))

pre = [0] * (n + 1)                      # pre[i] = 앞에서 i개의 합
for i in range(n):
    pre[i + 1] = pre[i] + a[i]

out = []
for _ in range(q):
    l, r = map(int, input().split())     # 1-indexed 구간 [l, r]
    out.append(str(pre[r] - pre[l - 1])) # 구간합 = 누적합의 뺄셈
print("\n".join(out))                    # 여러 줄은 모아서 한 번에 출력
