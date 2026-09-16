# Q03 파이썬 문법 노트 🐍

> 공통 문법은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. 튜플 `(d, c)` 과 리스트의 차이

```python
jobs.append((d, c))
```

괄호로 묶은 `(d, c)` 가 **튜플**. 리스트와 거의 같은데 **한 번 만들면 못 바꾼다**(immutable).

```python
t = (4, 20)
t[0]        # ✓ 4  — 읽기는 됨
t[0] = 5    # ✗ TypeError — 수정 불가
```

"마감일과 보상은 한 덩어리다"처럼 **의미가 묶인 값**엔 튜플을 쓴다.
덤으로 리스트보다 가볍고, 딕셔너리의 키나 `set` 의 원소로도 쓸 수 있다(리스트는 불가).

`append((d, c))` 의 **괄호 두 겹**에 주의. 안쪽은 튜플, 바깥쪽은 함수 호출 괄호다.
`append(d, c)` 라고 쓰면 인자를 2개 준 게 되어 TypeError.

### 2. 튜플 언패킹 (unpacking)

```python
for d, c in jobs:       # jobs 의 원소 (4, 20) 을 d=4, c=20 으로 쪼갠다
```

한 줄로 여러 변수에 나눠 담는 문법. `for` 뿐 아니라 어디서든 된다.

```python
d, c = (4, 20)          # d=4, c=20
a, b = b, a             # 스왑! 오른쪽이 먼저 전부 평가된다
```

개수가 안 맞으면 에러가 난다.
```python
d, c = (4, 20, 7)       # ✗ ValueError: too many values to unpack
```

### 3. 튜플 정렬 — 앞 원소부터 차례로 비교

```python
jobs.sort()
```

튜플 리스트를 그냥 정렬하면 **0번 원소로 먼저 비교하고, 같으면 1번 원소로** 비교한다.
여기선 마감일(`d`)이 0번이라 `sort()` 한 번으로 "마감일 오름차순"이 된다.

```python
[(4, 20), (1, 40), (1, 10)]  →  sort()  →  [(1, 10), (1, 40), (4, 20)]
                                                ↑ d 가 같으면 c 로 비교
```

특정 기준으로 정렬하고 싶으면 `key` 를 쓴다.
```python
jobs.sort(key=lambda x: x[1])         # 보상(1번 원소) 기준 오름차순
jobs.sort(key=lambda x: -x[1])        # 보상 내림차순 (부호를 뒤집는 트릭)
jobs.sort(key=lambda x: (x[0], -x[1]))  # 마감일 오름차순, 같으면 보상 내림차순
```

`sort()` 는 **원본을 바꾸고 None 을 반환**, `sorted()` 는 **새 리스트를 반환**한다.
```python
jobs = jobs.sort()      # ✗ jobs 가 None 이 된다! 최다 실수
jobs.sort()             # ✓
jobs = sorted(jobs)     # ✓
```

### 4. `heapq` — 리스트를 힙으로 쓰는 모듈

```python
import heapq
heap = []                       # 그냥 빈 리스트로 시작한다
heapq.heappush(heap, c)         # 넣기      O(log N)
x = heapq.heappop(heap)         # 최솟값 꺼내기 O(log N)
heap[0]                         # 최솟값 보기만 (안 꺼냄) O(1)
len(heap)                       # 개수
```

**전용 클래스가 아니라 평범한 리스트를 힙 규칙에 맞게 관리해주는 함수 모음**이다.
그래서 `heap` 을 `print` 해보면 완전히 정렬된 상태가 **아니다**. `heap[0]` 만 최솟값임이 보장된다.

```python
h = []
for x in [5, 1, 3]:
    heapq.heappush(h, x)
print(h)          # [1, 5, 3]  ← 정렬이 아니다. 하지만 h[0] 은 항상 최솟값
```

**파이썬 heapq 는 최소 힙만 있다.** 최대 힙이 필요하면 부호를 뒤집어 넣는다.
```python
heapq.heappush(h, -c)      # 넣을 때 마이너스
x = -heapq.heappop(h)      # 꺼낼 때 다시 마이너스 → 최댓값
```

튜플을 넣으면 튜플 비교 규칙대로 정렬된다 — 다익스트라에서 `(거리, 노드)` 를 넣는 이유.
```python
heapq.heappush(h, (dist, node))     # dist 가 작은 것부터 나온다
```

### 5. `len(heap) > d` — 개수로 조건 걸기

```python
if len(heap) > d:
    total -= heapq.heappop(heap)
```

`d` 일까지는 작업을 `d` 개까지 담을 수 있으니, **`d` 개를 넘었을 때만** 버린다.
`>=` 로 쓰면 담을 수 있는 걸 하나 더 버려서 답이 작아진다. **경계 하나 차이로 틀리는 전형적인 자리.**

헷갈리면 가장 작은 경우를 손으로 넣어보면 된다: `d=1` 이고 작업이 1개면
`len(heap)` 은 1 → `1 > 1` 은 False → 안 버림 → 맞다.
