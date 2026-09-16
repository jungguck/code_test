# Q06. 구간 안의 센서값 개수 ⭐⭐⭐ (실버 / 정렬 + 이분탐색)

## 문제
센서가 측정한 값 N개가 주어진다. (순서는 뒤죽박죽이고, 같은 값이 여러 번 나올 수 있다)

그리고 Q개의 질의가 들어온다. 각 질의는 두 정수 `L R` 이다.
**L 이상 R 이하인 값이 몇 개인지** 각각 출력하라.

## 입력
- 첫째 줄: N, Q  (1 ≤ N ≤ 200,000 / 1 ≤ Q ≤ 200,000)
- 둘째 줄: N개의 정수 `a_i`  (-10^9 ≤ a_i ≤ 10^9)
- 다음 Q개의 줄: `L R`  (-10^9 ≤ L ≤ R ≤ 10^9)

## 출력
- 각 질의의 답을 한 줄씩

## 예제 입력
```
7 3
1 5 3 9 5 2 8
1 5
4 9
10 20
```

## 예제 출력
```
5
4
0
```
> 정렬하면 `1 2 3 5 5 8 9`
> - `[1, 5]` → 1, 2, 3, 5, 5 → **5개**
> - `[4, 9]` → 5, 5, 8, 9 → **4개**
> - `[10, 20]` → 없음 → **0개**

## 접근법 — 정렬해두고 경계를 이분탐색으로 찾는다

질의마다 배열을 다 훑으면 O(N·Q) = 400억 → **시간 초과**.

핵심 발상:
> **한 번 정렬해두면**, "L 이상인 첫 위치" 와 "R 초과인 첫 위치" 만 알면
> 그 사이 개수는 **뺄셈 한 번**으로 나온다.

```
정렬: [1, 2, 3, 5, 5, 8, 9]
             ↑           ↑
        L=4 이상 첫 위치   R=9 초과 첫 위치
           (인덱스 3)       (인덱스 7)
        개수 = 7 - 3 = 4
```

### bisect 두 개의 차이 (여기가 핵심)
```python
import bisect
a = [1, 2, 3, 5, 5, 8, 9]

bisect.bisect_left(a, 5)    # → 3   5가 들어갈 "가장 왼쪽" 자리 = 5 이상인 첫 위치
bisect.bisect_right(a, 5)   # → 5   5가 들어갈 "가장 오른쪽" 자리 = 5 초과인 첫 위치
```
같은 값이 여러 개일 때 **left 는 그 앞, right 는 그 뒤**를 가리킨다.
그래서 답은:

```python
ans = bisect.bisect_right(a, R) - bisect.bisect_left(a, L)
```

정렬 O(N log N) + 질의마다 O(log N) → 전체 **O((N + Q) log N)**.

### 직접 구현한다면 (bisect 금지 버전)
```python
def lower_bound(a, x):
    """x 이상인 첫 인덱스를 찾는다. 없으면 len(a)"""
    lo, hi = 0, len(a)          # hi 는 "끝 다음 칸" 까지 잡는다
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1        # mid 는 답이 아니다 -> 오른쪽으로
        else:
            hi = mid            # mid 도 답일 수 있다 -> mid 를 버리지 않는다
    return lo
```
`hi = mid - 1` 이 아니라 **`hi = mid`** 인 것, 그리고 `lo < hi` (`<=` 아님) 가 짝이다.
`upper_bound` 는 `a[mid] < x` 를 `a[mid] <= x` 로만 바꾸면 된다.

## 함정 ⚠️
- **`bisect_left(L)` 와 `bisect_right(R)`** 조합이어야 한다.
  둘 다 left 로 쓰면 R과 같은 값들이 통째로 빠진다
- 정렬은 **딱 한 번**. 질의 안에서 정렬하면 O(Q·N log N) 으로 터진다
- 질의가 20만 개다. `print` 를 20만 번 호출하면 그것만으로 느리다.
  답을 리스트에 모아서 `sys.stdout.write("\n".join(...))` 로 **한 번에** 출력할 것
- 값이 음수도 된다. 인덱스로 세는 카운팅 배열은 못 쓴다

## 채점
```
python training/quiz/judge.py q06_range_count
```

---

## English version

### Q06. Counting Values in a Range (medium / sorting + binary search)

You are given **N** integers (unsorted, duplicates allowed) and **Q** queries. Each query
is a pair `L R`; for each one, print how many values lie **between L and R, inclusive**.

**Input** — The first line contains N and Q (1 ≤ N, Q ≤ 200,000). The second line contains
N integers (-10^9 ≤ a_i ≤ 10^9). Each of the next Q lines contains `L R`.

**Output** — One integer per query, each on its own line.

**Sample Input**
```
7 3
1 5 3 9 5 2 8
1 5
4 9
10 20
```
**Sample Output**
```
5
4
0
```

**Approach** — Sort the array once. Then each answer is
`bisect_right(a, R) - bisect_left(a, L)`: the index just past the last value ≤ R, minus
the index of the first value ≥ L. Sorting costs O(N log N) and each query O(log N).
Note the asymmetry — `bisect_left` for the lower bound, `bisect_right` for the upper.

> 단어장: inclusive(양끝 포함) / duplicates(중복) / query(질의)
> / lower bound(하한, x 이상 첫 위치) / upper bound(상한, x 초과 첫 위치) / sorted array(정렬된 배열)
