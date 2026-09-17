# Q11 파이썬 문법 노트 🐍

> 공통 문법(`input()`, `map`, 출력)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. `itertools.combinations` — 조합 만들기

```python
from itertools import combinations

for x, y, z in combinations(a, 3):
    ...
```

`combinations(a, 3)` 은 리스트 `a` 에서 **서로 다른 원소 3개를 고르는 모든 경우**를
순서대로 만들어 준다 (순서가 다른 건 같은 조합으로 친다).

```python
list(combinations([1,2,3,4], 2))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
```

- `combinations` : 순서 무시 (1,2) == (2,1)
- `permutations` : 순서 구분 (1,2) != (2,1)

### 2. `for x, y, z in ...` — 튜플 바로 언패킹

```python
for x, y, z in combinations(a, 3):     # (5,7,9) -> x=5, y=7, z=9
    s = x + y + z
```

각 조합이 3-튜플이므로 반복문에서 세 변수로 바로 풀어 받는다.

### 3. "지금까지의 최대" 를 변수로 갱신

```python
best = 0
for ...:
    s = x + y + z
    if s <= m and s > best:     # 조건 통과 + 더 크면
        best = s
```

`best` 에 **조건을 만족하는 값 중 가장 큰 것**을 계속 남긴다.
`and` 로 "M 이하" 와 "지금 최대보다 큼" 을 함께 검사한다.
([SYNTAX.md 6번](../SYNTAX.md) — `and` 는 왼쪽이 거짓이면 오른쪽을 건너뛴다)

## 삼중 for 로 직접 짜면 (itertools 없이)

```python
best = 0
for i in range(n):
    for j in range(i + 1, n):          # i 다음부터
        for k in range(j + 1, n):      # j 다음부터
            s = a[i] + a[j] + a[k]
            if s <= m and s > best:
                best = s
```

`j` 를 `i+1` 부터, `k` 를 `j+1` 부터 시작하는 게 **중복 없이 서로 다른 3개**를
고르는 관용구다. `combinations` 는 이걸 내부에서 대신 해 주는 것뿐이다.

## 왜 브루트포스로 충분한가

N=100이면 3개 조합은 `100·99·98 / 6 ≈ 161,700` 개.
16만 번은 파이썬으로도 순식간이라, 굳이 머리 쓸 필요 없이 **다 해보는 게 정답**이다.
"N이 작으면 완전탐색" 은 코테의 기본 감각이다.
