# 영어로 파이썬 코딩테스트 보기 🌐

> 결론부터: **영어 실력보다 "형식"이 훨씬 중요하다.**
> 한국(백준)은 `input()`/`print()` 인데, 영어권 플랫폼 대부분은 **함수 하나를 완성**하는 형식이다.
> 이거 모르고 들어가면 문제를 풀 줄 알아도 제출조차 못 한다.

---

## 1. 형식이 두 가지다 — 이게 제일 큰 차이

### A. 표준입출력형 (백준, Codeforces, AtCoder)
익숙한 그거. `sys.stdin` 으로 읽고 `print`.

```python
import sys
def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    print(sum(a))
main()
```

### B. 함수 완성형 (LeetCode, HackerRank, 실무 인터뷰 대부분) ⭐
**입력 파싱이 아예 없다.** 파라미터로 이미 들어와 있고 `return` 만 하면 된다.

```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}                       # value -> index
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []
```

**B에서 자주 하는 실수**
- `print` 로 답을 출력 → **0점**. 반드시 `return`
- `input()` 호출 → 테스트 러너가 멈춘다
- 빈 리스트/`None` 입력 처리 안 함 → 히든 테스트에서 떨어짐
- 타입 힌트(`List[int]`)는 장식이다. 지워도 되지만 **함수 이름·인자 순서는 절대 바꾸지 말 것**

> 훈련 요령: 우리 `training/quiz/` 문제를 풀 때, 정답을 한 번은
> `def solve(n, arr): return ...` 꼴의 **순수 함수**로 다시 짜 보기.
> 입출력과 알고리즘을 분리하는 습관이 B형식 대비의 전부다.

---

## 2. 제약조건 읽는 단어 (이것만 틀려도 통째로 틀린다)

| 영어 | 뜻 | 주의 |
|------|-----|------|
| at most / no more than | 최대 (이하) | `≤` |
| at least / no less than | 최소 (이상) | `≥` |
| exactly | 정확히 | 같음 |
| strictly increasing | 순증가 | 같은 값 불가 |
| non-decreasing | 비감소 | 같은 값 **허용** |
| distinct | 서로 다른 | 중복 없음 |
| non-negative | 음이 아닌 | **0 포함** |
| positive | 양수 | 0 제외 |
| inclusive | 포함 | `[a, b]` |
| exclusive | 미포함 | `[a, b)` |
| 0-indexed / 1-indexed | 인덱스 시작 | 문제마다 다르다 ⚠️ |
| contiguous / subarray | 연속 부분배열 | 붙어 있어야 함 |
| subsequence | 부분 수열 | **안 붙어 있어도 됨** |
| substring | 부분 문자열 | 붙어 있어야 함 |
| permutation | 순열 | 순서 바꾼 것 |
| lexicographically smallest | 사전순으로 가장 작은 | 문자열 비교 |
| in-place | 제자리에서 | **새 배열 만들면 안 됨** |
| guaranteed | 보장됨 | 그 예외는 처리 안 해도 됨 |

**`subarray` vs `subsequence` 를 헷갈리면 완전히 다른 문제를 푼다.** 여기가 제일 자주 깨지는 지점.

---

## 3. 문제 지문 상투 표현

| 표현 | 뜻 |
|------|-----|
| Return the minimum number of operations | 최소 연산 횟수를 반환하라 |
| It is guaranteed that a solution exists | 답이 반드시 존재한다 |
| If no such X exists, return -1 | 없으면 -1 |
| The answer may be large, return it modulo 10^9 + 7 | 큰 수는 나머지로 |
| Two subarrays are considered different if ... | 무엇을 "다른 것"으로 셀지 |
| The test cases are generated such that ... | 그런 입력만 들어온다 |
| Can you solve it in O(n) time and O(1) space? | 팔로업(추가 질문) |
| Follow-up: | 통과 후 더 어려운 조건 |

---

## 4. 외워둘 파이썬 무기고 (영어권 문제는 표준 라이브러리를 대놓고 기대한다)

```python
from collections import deque, defaultdict, Counter
import heapq, bisect, math
from functools import lru_cache
from itertools import permutations, combinations, accumulate

deque()                       # BFS 큐. popleft() 가 O(1)
defaultdict(list)             # 그래프 인접리스트
Counter(words).most_common(1) # 최빈값
heapq.heappush / heappop      # 최소 힙 (최대 힙은 값에 -1 곱하기)
bisect.bisect_left(arr, x)    # 정렬된 배열 이분탐색 -> LIS, 파라메트릭
math.gcd(a, b)                # 최대공약수
list(accumulate(a))           # 누적합 한 줄
@lru_cache(maxsize=None)      # 재귀 DP 메모이제이션
sys.setrecursionlimit(10**6)  # 깊은 재귀 (파이썬 기본 1000)
```

**빈출 패턴 5개** — 영어권 인터뷰 문제의 절반 이상이 여기서 나온다:
1. Hash map 으로 O(n²) → O(n) (two sum, 그룹핑)
2. Two pointers / sliding window (연속 구간)
3. BFS/DFS on grid or graph (최단거리, 연결요소)
4. Heap (top-K, 스케줄링)
5. Binary search on the answer (파라메트릭 서치)

→ `training/quiz/` 의 Q02(윈도우), Q03(힙), Q04(BFS), Q05(해시/누적합)가 정확히 이 패턴이다.

---

## 5. 말로 설명해야 하는 경우 (라이브 인터뷰)

영어 인터뷰는 **코드보다 설명**이다. 통문장으로 외워두면 된다.

**질문 확인**
- "Just to clarify — can the input array be empty?"
- "Are the values guaranteed to be distinct?"
- "Should I optimize for time or memory?"

**접근 설명**
- "My first thought is the brute-force approach: check every pair, which is O(n²)."
- "I can do better by using a hash map to look up complements in constant time."
- "This brings the total complexity down to O(n) time and O(n) space."
- "Let me walk through the example to make sure it works."

**엣지 케이스**
- "Let me handle the edge case where the array has only one element."
- "I'll add a guard for the empty input."

**막혔을 때 (침묵보다 100배 낫다)**
- "Let me think out loud for a second."
- "I'm considering two options here — sorting first, or using a heap."

---

## 6. 플랫폼별 한 줄 요약

| 플랫폼 | 형식 | 특징 |
|--------|------|------|
| LeetCode | 함수 완성 | 영어권 인터뷰 표준. 여기만 해도 됨 |
| HackerRank | 함수 완성 (가끔 stdin) | 회사 채용에서 많이 씀 |
| Codility | 함수 완성 | 유럽 기업. 엣지 케이스 배점이 큼 |
| CodeSignal | 함수 완성 | 시간 압박 강함 |
| Codeforces | 표준입출력 | 대회형, 난이도 높음 |

---

## 7. 이번 주 추천 훈련 루틴

1. `training/quiz/` 문제를 **한글 지문으로** 푼다 (알고리즘 훈련)
2. 같은 문제를 각 `problem.md` 의 **English version 만 읽고** 다시 푼다 (지문 독해 훈련)
3. 정답을 **`class Solution:` 함수형으로** 옮겨 적는다 (형식 훈련)
4. 접근법을 위 5번의 문장들로 **영어로 소리 내어** 30초 설명한다 (인터뷰 훈련)

하루 한 문제 × 4단계면 충분하다. 문제 개수보다 4단계를 다 하는 게 중요.
