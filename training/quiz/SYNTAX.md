# 코테 파이썬 문법 — 공통편 🐍

> 모든 quiz 문제의 `solution.py` 가 공통으로 쓰는 문법.
> 문제별로 새로 나오는 문법은 각 폴더의 `syntax.md` 에 있다.

---

## 1. 입력 읽기 — `input = sys.stdin.readline`

```python
import sys
input = sys.stdin.readline      # 파일 맨 위에 딱 한 줄
```

이 한 줄만 넣으면 **평소 쓰던 `input()` 그대로** 쓰면서 속도만 빨라진다.

```python
n = int(input())                        # 숫자 하나
n, m = map(int, input().split())        # 한 줄에 숫자 여러 개
a = list(map(int, input().split()))     # 한 줄에 숫자 N개
s = input().strip()                     # 문자열 한 줄
```

### 왜 바꾸는가
기본 `input()` 은 호출할 때마다 프롬프트 처리 등 부가 작업을 한다.
한두 번이면 티가 안 나지만 **10만 줄을 읽으면 그것만으로 몇 초**가 날아간다.
`sys.stdin.readline` 은 그 과정을 건너뛴다. 코테에서 "시간 초과인데 알고리즘은 맞는 것 같다" 면
십중팔구 여기다.

### ⚠️ 주의 1 — 개행문자가 딸려온다
`readline` 은 줄 끝의 `\n` 까지 **그대로** 준다.

```python
# 입력이 "abc\n" 일 때
input()           # 'abc\n'   ← 줄바꿈이 붙어있다!
input().strip()   # 'abc'     ✓
```

숫자는 신경 안 써도 된다. `int()` 와 `split()` 이 공백·개행을 알아서 무시한다.
**문자열로 쓸 때만 `.strip()`** 을 붙이면 된다. (격자 문제에서 이거 빼먹으면 조용히 틀린다)

### ⚠️ 주의 2 — 덮어쓰기다
`input = sys.stdin.readline` 은 원래 `input` 이라는 이름에 **다른 함수를 덮어씌우는 것**이다.
괄호 `()` 를 안 붙이는 데 주의.

```python
input = sys.stdin.readline()    # ✗ 지금 한 줄 읽어서 그 결과(문자열)를 담아버린다
input = sys.stdin.readline      # ✓ 함수 자체를 담는다
```

### 참고 — 더 빠른 방법도 있다 (지금은 몰라도 됨)
입력이 100만 줄쯤 되면 이런 것도 쓴다.
```python
data = sys.stdin.buffer.read().split()    # 입력 전체를 통째로 읽어 토큰 리스트로
```
줄 구분이 사라져서 `data[0]`, `data[1]` 처럼 **순서대로 꺼내 써야** 한다.
빠르지만 읽기 어려워서, 이 훈련장에서는 쓰지 않는다.

---

## 2. 한 줄에서 여러 값 받기

```python
n, m = map(int, input().split())
```

세 단계로 쪼개서 보면 이렇다.

```python
input()            # '4 5\n'
      .split()     # ['4', '5']      공백으로 쪼갠다 (개행도 알아서 처리)
map(int, ...)      # 각 원소에 int() 를 적용
n, m = ...         # 왼쪽 변수들에 하나씩 나눠 담는다 (언패킹)
```

**개수가 안 맞으면 에러**가 난다.
```python
n, m = map(int, "4 5 6".split())    # ✗ ValueError: too many values to unpack
```

### `list()` 를 언제 씌우는가
`map` 은 리스트가 아니라 **한 번만 훑고 사라지는 반복자**다.

```python
a = map(int, input().split())
a[0]            # ✗ TypeError: 'map' object is not subscriptable

a = list(map(int, input().split()))
a[0]            # ✓
```

- `n, m = map(...)` → 바로 풀어서 담으니까 `list()` **불필요**
- `a = list(map(...))` → 나중에 `a[i]` 로 접근하니까 `list()` **필요**

---

## 3. 출력

```python
print(a, b)        # "20 2"   — 콤마 자리에 공백이 들어간다
print(*nums)       # 리스트를 풀어서 공백 구분으로 출력
```

답이 **여러 줄**이면 `print` 를 여러 번 부르지 말고 모아서 한 번에 내보낸다.
`print` 는 호출 자체가 비싸서, 20만 번 부르면 그것만으로 몇 초가 걸린다.

```python
answers = []
for ...:
    answers.append(답)
print("\n".join(map(str, answers)))
```

`join` 은 **문자열만** 받는다. 숫자 리스트면 반드시 `map(str, ...)` 을 거칠 것.
```python
"\n".join([1, 2, 3])              # ✗ TypeError
"\n".join(map(str, [1, 2, 3]))    # ✓ "1\n2\n3"
```

---

## 4. `_` (언더바)

```python
for _ in range(n):
```
특별한 문법이 아니라 **그냥 변수 이름**이다. `for i in range(n)` 과 똑같이 동작한다.
"이 변수는 안 쓸 거예요"라는 관습적 표시일 뿐.

---

## 5. "비어 있는 것은 거짓" (truthy / falsy)

```python
while q:           # 큐에 뭔가 있는 동안
if not stack:      # 스택이 비었으면
```

파이썬은 아래를 전부 **False** 로 친다:
```
0        0.0        ''        []        {}        ()       None
```
그래서 `len(q) > 0` 대신 그냥 `q`, `len(stack) == 0` 대신 `not stack` 이라고 쓴다.

---

## 6. `and` / `or` 의 단락 평가 (short-circuit) ⭐

**`and` 는 왼쪽이 거짓이면 오른쪽을 실행조차 안 한다.** `or` 는 왼쪽이 참이면 마찬가지.

이게 문법 지식이 아니라 **에러 방지 도구**로 쓰인다.

```python
if 0 <= i < n and arr[i] == x:     # ✓ 범위 확인이 먼저 → 안전
if arr[i] == x and 0 <= i < n:     # ✗ 범위 밖이면 IndexError 로 죽는다
```

**"안전한지 먼저 확인 → 그 다음에 접근"** 순서. 코테에서 무한히 반복되는 패턴이다.

---

## 7. `continue` 로 조건을 한 줄씩 걸러내기

조건을 `and` 로 길게 잇는 대신, **아닌 경우를 위에서 하나씩 쳐내면** 읽기 쉬워진다.

```python
# ✗ 한 줄이 길어서 어디가 틀렸는지 안 보인다
if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and grid[nr][nc] == '1':
    ...

# ✓ 이유별로 한 줄씩
if nr < 0 or nr >= n:
    continue          # 위아래로 격자 밖
if visited[nr][nc]:
    continue          # 이미 가본 칸
...
```

`continue` 는 **이번 반복만 건너뛰고 다음 반복으로** 간다 (`break` 는 루프를 완전히 탈출).
들여쓰기가 깊어지는 걸 막아줘서 **early continue** 라고 부른다.

---

## 8. 자주 만나는 에러와 원인

| 에러 | 대표 원인 |
|------|----------|
| `IndexError: list index out of range` | 범위 체크를 배열 접근보다 늦게 함 / 빈 리스트에 `pop()` |
| `ValueError: too many values to unpack` | `n, m = ...` 인데 오른쪽 값 개수가 다름 |
| `ValueError: invalid literal for int()` | 빈 줄이나 문자를 `int()` 함 (`.strip()` 누락 포함) |
| `TypeError: sequence item 0: expected str instance, int found` | `"\n".join(숫자리스트)` → `map(str, ...)` 빠뜨림 |
| `TypeError: 'map' object is not subscriptable` | `map` 에 `list()` 를 안 씌우고 인덱스 접근 |
| `RecursionError` | 깊은 재귀 DFS. **BFS(deque)로 바꿔라** |
| 답은 맞는데 **시간 초과** | `input()` 그대로 씀 / `print` 반복 / 리스트 `.pop(0)` |
