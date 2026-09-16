# Q05. M의 배수 구간 세기 ⭐⭐⭐⭐ (골드 / 누적합 + 나머지) 🔥

## 문제
길이 N의 수열 `a_1 ... a_N` 이 주어진다.
**연속한 부분 수열** 중에서, 원소의 합이 **M의 배수**인 것의 **개수**를 구하라.

부분 수열 `(i, j)` 는 `i ≤ j` 인 구간 `a_i + a_{i+1} + ... + a_j` 를 뜻한다.
`(i, j)` 가 다르면 합이 같아도 다른 것으로 센다.

## 입력
- 첫째 줄: N, M  (1 ≤ N ≤ 1,000,000 / 2 ≤ M ≤ 1,000)
- 둘째 줄: N개의 정수 `a_i`  (0 ≤ a_i ≤ 10^9)

## 출력
- 합이 M의 배수인 연속 부분 수열의 개수

## 예제 입력
```
5 3
1 2 3 1 2
```

## 예제 출력
```
7
```

### 왜 7인가
```
(1,2)=3   (1,3)=6   (1,5)=9
(2,3)=6
(3,3)=3   (3,5)=6
(4,5)=3
```

## 예제 입력 2
```
4 2
2 4 6 8
```
## 예제 출력 2
```
10
```
> 전부 짝수라 모든 구간(4+3+2+1 = 10개)이 답

## 접근법 — 누적합을 "나머지" 로 접는다

### 1단계: 구간합을 누적합 차이로
```
P[0] = 0,  P[i] = a_1 + ... + a_i
구간 (i, j) 의 합 = P[j] - P[i-1]
```

### 2단계: 배수 조건을 나머지 조건으로
```
(P[j] - P[i-1]) % M == 0
   <=>   P[j] % M == P[i-1] % M
```
즉 **나머지가 같은 누적합 두 개를 고르면 그 사이 구간은 항상 M의 배수**다.
구간을 세는 문제가 → **"나머지가 같은 누적합 쌍의 개수"** 문제로 바뀐다.

### 3단계: 쌍의 개수 세기
나머지 r을 가진 누적합이 `c_r` 개 있으면, 거기서 두 개를 고르는 경우의 수는
```
C(c_r, 2) = c_r * (c_r - 1) / 2
```
답은 모든 r에 대해 이걸 더한 값.

```
cnt = [0] * M
cnt[0] = 1           # P[0] = 0 도 반드시 세어야 한다  ← 가장 흔한 실수
s = 0
각 a 에 대해:
    s = (s + a) % M
    cnt[s] += 1
답 = sum(c * (c - 1) // 2 for c in cnt)
```

전체 **O(N + M)**. 구간을 하나씩 다 보면 O(N²) = 10^12 → 절대 불가능.

## 함정 ⚠️
- **`P[0] = 0` 을 빼먹으면** 앞에서부터 시작하는 구간((1,j) 꼴)을 통째로 놓친다.
  예제 1에서 이걸 빼먹으면 7이 아니라 4가 나온다
- 누적합을 그대로 들고 있지 말고 **매번 `% M`** 을 해라. (파이썬은 큰 정수라
  틀리진 않지만 느려진다. C++/자바면 오버플로로 틀린다)
- 답은 최대 약 `N*(N+1)/2` ≈ 5×10^11 → 64비트 필요
- 구간을 하나씩 다 확인하면 O(N²) = 10^12 이라 절대 못 푼다. 누적합으로 한 번만 훑을 것

## 보너스 (더 어렵게)
합이 M의 배수인 구간 중 **가장 긴 것의 길이**도 구해보라.
(힌트: 각 나머지가 **처음 등장한 인덱스**만 기억하면 된다)

## 채점
```
python training/quiz/judge.py hard02_mod_subarray
```

---

## English version

### Q05. Subarrays Divisible by M (hard / prefix sums + modular counting)

Given an array of **N** non-negative integers, count the number of **contiguous
subarrays whose sum is divisible by M**. Two subarrays are different if their index
ranges differ.

**Input** — The first line contains N and M (1 ≤ N ≤ 1,000,000; 2 ≤ M ≤ 1,000).
The second line contains N integers (0 ≤ a_i ≤ 10^9).

**Output** — The count of such subarrays.

**Sample Input**
```
5 3
1 2 3 1 2
```
**Sample Output**
```
7
```

**Approach** — Let `P[i]` be the prefix sum of the first i elements. A subarray `(i, j)`
is divisible by M exactly when `P[j] ≡ P[i-1] (mod M)`. So count how many prefix sums
fall into each residue class r, and add `C(c_r, 2)` for each. **Remember to count
`P[0] = 0`** — forgetting it silently drops every subarray that starts at index 1.
Total time O(N + M).

> 단어장: divisible by(~로 나누어떨어지는) / remainder, residue(나머지)
> / prefix sum(누적합) / pair(쌍) / overflow(자리 넘침) / non-negative(음이 아닌)
