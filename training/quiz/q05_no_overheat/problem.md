# Q05. 과열 없이 작업하기 ⭐⭐⭐ (실버 / 1차원 DP)

## 한 줄 요약
> **붙어 있는 두 날은 동시에 고를 수 없다. 고른 날들의 합을 최대로 만들어라.**

## 문제
로봇이 N일 동안 일한다. i일째에 작업하면 `a_i` 만큼의 성과를 얻는다.

이 로봇은 **이틀 연속으로 작업하면 과열되어 고장난다.**
그래서 어떤 날 작업했으면 **바로 다음 날은 반드시 쉬어야** 한다.
(쉬는 날은 성과가 0. 며칠을 내리 쉬어도 상관없고, 아무 날도 안 골라도 된다)

즉 **어느 날에 일할지 골라야 하는데, 고른 날들끼리 이웃하면 안 된다.**
그렇게 고른 날들의 **성과 합의 최댓값**을 구하라.

### 그림으로
`a = [10, 5, 20, 30, 1]` 일 때 고를 수 있는 것과 없는 것:

```
        1일  2일  3일  4일  5일
성과:    10   5   20   30    1

 O       ■    .    ■    .    ■     10+20+1 = 31    (1·3·5일 — 다 떨어져 있음)
 O       ■    .    .    ■    .     10+30   = 40    ← 최대
 O       .    ■    .    ■    .      5+30   = 35
 X       .    .    ■    ■    .     3일과 4일이 붙어있음 -> 과열!
 X       ■    ■    .    .    .     1일과 2일이 붙어있음 -> 과열!
```
`■` = 작업하는 날, `.` = 쉬는 날.

### 왜 "큰 것부터 고르기"로는 안 되는가
`a = [4, 5, 4, 5, 4]` 를 보자.
- 큰 것부터: 5(2일) → 5(4일) → **10**. 2일과 4일을 골랐으니 1·3·5일은 전부 옆자리라 못 쓴다
- 정답: 1·3·5일의 **4 + 4 + 4 = 12**

**지금 고른 것이 옆자리를 막아버리기 때문에**, 눈앞의 큰 값만 보면 틀린다.
이래서 그리디가 아니라 DP 로 풀어야 한다.

## 입력
- 첫째 줄: N  (1 ≤ N ≤ 100,000)
- 둘째 줄: N개의 정수 `a_1 ... a_N`  (0 ≤ a_i ≤ 10,000)

## 출력
- 최대 성과 합

## 예제 입력
```
5
10 5 20 30 1
```

## 예제 출력
```
40
```
> 1일(10)과 4일(30)을 골랐을 때가 최대. 위 그림의 두 번째 줄.

## 예제 입력 2
```
4
5 5 5 5
```
## 예제 출력 2
```
10
```
> 1일과 3일 (또는 1일과 4일, 2일과 4일) → 10

## 접근법 — 점화식 세우기

### 왜 그리디가 안 되는가
"큰 것부터 고르면 되지" 싶지만 틀린다. `10 5 20 30 1` 에서 제일 큰 30을 고르면
3일(20)을 못 쓴다. **지금의 선택이 미래를 막는다** → DP.

### 상태를 정의한다
```
dp[i] = "i일째까지만 봤을 때 얻을 수 있는 최대 성과"
```
여기서 "i일에 작업했는지 안 했는지"는 굳이 나눌 필요가 없다. **i일까지의 최선**만 기억하면 된다.

### 점화식 — i일에 대해 선택지는 딱 두 개
```
① i일에 쉰다   -> 어제까지의 최선 그대로        = dp[i-1]
② i일에 일한다 -> 어제는 무조건 쉬었어야 하므로  = dp[i-2] + a[i]

dp[i] = max(dp[i-1], dp[i-2] + a[i])
```

②에서 `dp[i-1]` 이 아니라 **`dp[i-2]`** 를 쓰는 게 이 문제의 전부다.
i일에 일하려면 i-1일은 비어 있어야 하니까, i-2일까지의 최선에 이어 붙이는 것.

### 초기값
```
dp[0] = a[0]                      # 첫날은 그냥 일하면 됨
dp[1] = max(a[0], a[1])           # 이틀 중 큰 거 하나만
```

### 메모리 줄이기 (보너스)
`dp[i]` 는 바로 앞 두 개만 보니까 배열 없이 변수 두 개면 된다.
```python
prev2, prev1 = 0, 0
for x in a:
    prev2, prev1 = prev1, max(prev1, prev2 + x)
print(prev1)
```
O(N) 시간 / **O(1) 메모리**. 영어권 인터뷰에서 "Can you do it in O(1) space?" 로
자주 나오는 팔로업이 정확히 이거다.

## 함정 ⚠️
- **N = 1** 일 때 `dp[1]` 을 만들려다 인덱스 에러가 난다. 따로 처리하거나 위 2변수 버전을 쓸 것
- `a_i` 가 0일 수 있다. "무조건 일하는 게 이득" 이 아닌 경우가 생긴다
- 이 문제의 정식 이름은 **House Robber** (이웃한 집은 못 턴다). 영어 문제로 그대로 나온다

## 채점
```
python training/quiz/judge.py q05_no_overheat
```

---

## English version

### Q05. No Two Days in a Row (medium / 1-D dynamic programming)

A robot works for **N** days; working on day i yields `a_i` points. The robot
**cannot work on two consecutive days** — after a working day it must rest.
Resting yields 0 points, and any number of consecutive rest days is allowed.
Print the **maximum total points**.

**Input** — The first line contains N (1 ≤ N ≤ 100,000). The second line contains
N integers (0 ≤ a_i ≤ 10,000).

**Output** — A single integer, the maximum total.

**Sample Input**
```
5
10 5 20 30 1
```
**Sample Output**
```
40
```

**Approach** — Let `dp[i]` be the best total considering only the first i days.
On day i you either rest (`dp[i-1]`) or work, which forces day i-1 to be a rest day
(`dp[i-2] + a[i]`). So `dp[i] = max(dp[i-1], dp[i-2] + a[i])`. Since only the last two
values matter, two variables are enough — **O(N) time, O(1) space**.
This is the classic **House Robber** problem.

> 단어장: consecutive(연속된) / yield(내놓다, 산출하다) / recurrence relation(점화식)
> / subproblem(부분 문제) / optimal(최적의) / follow-up(추가 질문) / in O(1) space(상수 메모리로)
