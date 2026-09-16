# 코테 파이썬 문법 — 공통편 🐍

> 모든 quiz 문제의 `solution.py` 가 공통으로 쓰는 문법.
> 문제별로 새로 나오는 문법은 각 폴더의 `syntax.md` 에 있다.

---

## 1. 입력 읽기 — `input()`

```python
n = int(input())                        # 숫자 하나
n, m = map(int, input().split())        # 한 줄에 숫자 여러 개
a = list(map(int, input().split()))     # 한 줄에 숫자 N개
s = input()                             # 문자열 한 줄
```

규칙은 딱 두 개다.

1. **한 번 호출 = 한 줄.** 다음 `input()` 은 자동으로 다음 줄을 읽는다
2. **줄 끝 개행(`\n`)은 알아서 떼어준다.** 그래서 `.strip()` 을 붙일 필요가 없다

그래서 **문제 지문의 줄 구성이 곧 코드의 `input()` 호출 횟수**가 된다.
지문을 그대로 코드로 옮긴다고 생각하면 된다.

```
첫째 줄에 N, M          ->  n, m = map(int, input().split())
둘째 줄에 N개의 정수    ->  a = list(map(int, input().split()))
다음 N개의 줄에 ...     ->  for _ in range(n):
                                ... = input()
```

### 한 번의 호출은 한 줄까지만

값이 다음 줄로 넘어가 있으면 한 번의 `input()` 으로는 못 가져온다.

```python
n, m = map(int, input().split())
# 입력이 "5 50"   (같은 줄)  -> ✓ n=5, m=50
# 입력이 "5"⏎"50" (줄 나뉨)  -> ✗ ValueError: not enough values to unpack
```

줄이 나뉘어 있으면 호출도 나눈다.
```python
n = int(input())
m = int(input())
```

### 속도는 신경 쓰지 않아도 된다
입력이 20만 줄이어도 읽는 데 0.15초다. 시간 초과가 난다면 입력이 아니라
**알고리즘이 O(N²)라서**일 가능성이 훨씬 크다.

## 2. 한 줄에서 여러 값 받기

```python
n, m = map(int, input().split())
```

세 단계로 쪼개서 보면 이렇다.

```python
input()            # '4 5'
      .split()     # ['4', '5']      공백으로 쪼갠다
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
| `ValueError: invalid literal for int()` | 빈 줄이나 문자를 `int()` 함 / 읽는 줄 수가 어긋남 |
| `TypeError: sequence item 0: expected str instance, int found` | `"\n".join(숫자리스트)` → `map(str, ...)` 빠뜨림 |
| `TypeError: 'map' object is not subscriptable` | `map` 에 `list()` 를 안 씌우고 인덱스 접근 |
| `RecursionError` | 깊은 재귀 DFS. **BFS(deque)로 바꿔라** |
| 답은 맞는데 **시간 초과** | `print` 를 수십만 번 호출 / 리스트 `.pop(0)` / 알고리즘이 O(N²) |
