# Q03. 마감일 작업 스케줄링 ⭐⭐⭐ (실버~골드 / 그리디 + 우선순위 큐)

## 문제
로봇에게 N개의 작업이 들어왔다. i번째 작업은
- **마감일 `d_i`** — `d_i`일째 되는 날까지(포함) 처리해야 한다
- **보상 `c_i`** — 처리하면 받는 값

로봇은 **하루에 정확히 한 작업**만 처리할 수 있고, 1일차부터 시작한다.
작업을 포기해도 된다.

받을 수 있는 **보상의 합의 최댓값**을 구하라.

## 입력
- 첫째 줄: N (1 ≤ N ≤ 200,000)
- 다음 N개의 줄: `d_i c_i`  (1 ≤ d_i ≤ 200,000 / 1 ≤ c_i ≤ 1,000,000)

## 출력
- 최대 보상 합 (한 줄)

## 예제 입력
```
4
4 20
1 10
1 40
1 30
```

## 예제 출력
```
60
```
> 1일차 마감인 작업이 3개(10, 40, 30)지만 1일차엔 하나만 가능 → 40 선택.
> 4일차 마감 작업 20은 2일차에 해도 되니까 챙긴다. 40 + 20 = 60

## 예제 입력 2
```
5
2 10
2 20
2 30
3 5
1 100
```
## 예제 출력 2
```
135
```
> 1일: 100(마감 1일), 2일: 30, 3일: 5 → 135.
> 마감 2일짜리 세 개(10/20/30) 중에는 **하나만** 더 할 수 있다 (1일차는 100이 먹었으니까).

## 접근법 — "일단 넣고, 넘치면 제일 싼 걸 버린다"

### 왜 그리디가 되는가
마감일 순으로 정렬하고 앞에서부터 보면,
**마감일이 d인 작업들까지 고려했을 때 고를 수 있는 개수는 최대 d개**다.
(1일차 ~ d일차, 총 d칸)

그래서 이렇게 한다:
```
마감일 오름차순으로 정렬
힙(최소 힙) = 지금까지 "채택한" 작업들의 보상
각 작업 (d, c) 에 대해:
    힙에 c 를 넣는다                     # 일단 채택
    if 힙 크기 > d:                      # 칸이 모자라면
        힙에서 가장 작은 보상을 버린다     # 제일 손해 적은 걸 포기
답 = 힙에 남은 보상의 합
```

**핵심**: 나중에 더 비싼 작업이 나오면 그때 이미 넣어둔 싼 걸 빼면 된다.
→ 결정을 **미룰 수 있어서** 그리디가 안전해진다. (교환 논법)

### 왜 최소 힙인가
"남은 것 중 제일 작은 보상"을 매번 꺼내야 하는데,
리스트에서 매번 min 찾으면 O(N²). 힙이면 넣기/빼기 둘 다 O(log N) → 전체 **O(N log N)**.

```python
import heapq
heapq.heappush(h, c)    # 넣기
heapq.heappop(h)        # 가장 작은 값 꺼내기 (파이썬 heapq 는 최소 힙)
```

## 함정 ⚠️
- 마감일이 같은 작업끼리의 순서는 상관없다. `d` 기준 정렬만 하면 된다
- `힙 크기 > d` 지 `>= d` 가 아니다. d일까지면 d개는 담을 수 있다
- 보상을 다 더하면 2×10^11 — 파이썬은 큰 정수라 괜찮지만 C++/자바면 `long long`
- 입력이 20만 줄이다. `input = sys.stdin.readline` 을 반드시 넣을 것

## 채점
```
python training/quiz/judge.py q03_job_schedule
```

---

## English version

### Q03. Deadline Scheduling (medium-hard / greedy + priority queue)

There are **N** jobs. Job i has a **deadline `d_i`** (it must be done on day `d_i` or
earlier) and a **profit `c_i`**. Exactly **one job per day** can be processed, starting
from day 1. Jobs may be skipped. Print the **maximum total profit**.

**Input** — The first line contains N (1 ≤ N ≤ 200,000). Each of the next N lines
contains `d_i c_i` (1 ≤ d_i ≤ 200,000; 1 ≤ c_i ≤ 1,000,000).

**Output** — A single integer, the maximum total profit.

**Sample Input**
```
4
4 20
1 10
1 40
1 30
```
**Sample Output**
```
60
```

**Approach** — Sort jobs by deadline ascending. Push each profit onto a **min-heap**;
whenever the heap size exceeds the current deadline, pop the smallest profit (discard
the least valuable job accepted so far). The heap's final sum is the answer. O(N log N).

> 단어장: deadline(마감일) / profit(이익) / at most one job per day(하루 최대 한 작업)
> / min-heap(최소 힙) / discard(버리다) / ascending order(오름차순) / exceed(넘다)
