# Q02. 최소 이동 구간 ⭐⭐⭐ (실버 / 투 포인터)

## 문제
로봇이 N개의 구간을 순서대로 지나간다. i번째 구간의 길이는 `a_i` 다.
**연속한 구간들**만 골라서 이동 거리의 합이 **S 이상**이 되게 하려고 한다.

조건을 만족하는 연속 구간들 중 **개수가 가장 적은 것**의 개수를 출력하라.
아무리 다 합쳐도 S를 못 넘기면 `0` 을 출력한다.

## 입력
- 첫째 줄: N, S  (1 ≤ N ≤ 200,000 / 1 ≤ S ≤ 100,000,000)
- 둘째 줄: N개의 정수 `a_1 ... a_N`  (1 ≤ a_i ≤ 10,000)

## 출력
- 합이 S 이상이 되는 가장 짧은 연속 구간의 길이 (없으면 0)

## 예제 입력
```
10 15
5 1 3 5 10 7 4 9 2 8
```

## 예제 출력
```
2
```
> `10 7` 두 개로 17 ≥ 15. 한 개짜리는 최대 10이라 불가능 → 답 2

## 예제 입력 2
```
5 100
1 2 3 4 5
```
## 예제 출력 2
```
0
```

## 접근법 — 투 포인터 (슬라이딩 윈도우)

모든 (시작, 끝) 쌍을 다 보면 O(N²) = 400억 → **시간 초과**.

핵심 성질 한 줄:
> `a_i` 가 전부 **양수**라서, 창을 **오른쪽으로 늘리면 합은 커지고 / 왼쪽을 당기면 합은 작아진다.**
> 그래서 되돌아갈 필요가 없다.

```
left = 0, total = 0, best = 무한대
right 를 0 → N-1 로 옮기며:
    total += a[right]                       # 창을 오른쪽으로 한 칸 늘린다
    while total >= S:                       # 조건을 만족하는 동안
        best = min(best, right - left + 1)  # 길이 갱신하고
        total -= a[left]; left += 1         # 왼쪽을 줄여서 "더 짧게" 시도
```

`left` 와 `right` 가 각각 **N번만 전진**하므로 전체 O(N).
`while` 이 안쪽에 있다고 O(N²)가 아니다 — `left` 는 절대 뒤로 안 가기 때문.

## 함정 ⚠️
- `if` 가 아니라 **`while`** 이어야 한다. 한 칸 늘렸을 때 왼쪽을 여러 칸 당길 수 있다
- 답이 갱신된 적 없으면 0 출력 (무한대 그대로 찍으면 안 됨)
- 기본 `input()` 을 그대로 쓰면 안 된다. N이 20만이라 **입력 읽는 것만으로** TLE 가 난다.
  맨 위에 `input = sys.stdin.readline` 한 줄을 넣을 것

## 채점
```
python training/quiz/judge.py q02_min_window
```

---

## English version

### Q02. Shortest Segment (medium / two pointers)

You are given a sequence of **N** positive integers `a_1 ... a_N` and a target **S**.
Find the length of the **shortest contiguous subarray** whose sum is **greater than or
equal to S**. If no such subarray exists, print `0`.

**Input** — The first line contains N and S (1 ≤ N ≤ 200,000; 1 ≤ S ≤ 100,000,000).
The second line contains N integers (1 ≤ a_i ≤ 10,000).

**Output** — Print the minimum length, or 0 if there is none.

**Sample Input**
```
10 15
5 1 3 5 10 7 4 9 2 8
```
**Sample Output**
```
2
```

> 단어장: contiguous subarray(연속 부분 수열) / greater than or equal to(이상)
> / shrink the window(창을 줄이다) / two pointers(투 포인터) / time limit exceeded(시간 초과)
