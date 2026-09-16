# 코테 파이썬 문법 — 공통편 🐍

> 모든 quiz 문제의 `solution.py` 가 공통으로 쓰는 문법.
> 문제별로 새로 나오는 문법은 각 폴더의 `syntax.md` 에 있다.

---

## 1. 입력 읽기 — 세 가지 방식과 속도 차이

```python
# ① 기본 (느림) — 줄 수가 100줄 이하일 때만
n = int(input())

# ② readline (빠름) — 줄 단위로 읽어야 할 때
import sys
input = sys.stdin.readline
n = int(input())

# ③ 통째로 읽기 (제일 빠름) — quiz 문제들이 쓰는 방식
import sys
data = sys.stdin.buffer.read().split()
```

③이 하는 일을 한 단계씩 뜯어보면:

```python
sys.stdin.buffer.read()        # 입력 전체를 bytes 하나로   b'5 50\n-30 -40 60\n'
                     .split()  # 공백/줄바꿈으로 전부 쪼갬   [b'5', b'50', b'-30', ...]
```

**줄 구분이 사라진다**는 게 포인트다. `5 50\n-30` 이든 `5\n50\n-30` 이든 결과가 같아서,
"첫 줄에 N, 둘째 줄에 N개" 같은 형식을 신경 쓸 필요가 없다. 앞에서부터 순서대로 꺼내 쓰면 된다.

```python
n = int(data[0])            # 0번째 토큰
b = int(data[1])            # 1번째 토큰
a = list(map(int, data[2:2 + n]))   # 2번째부터 n개
```

### `buffer` 가 뭔데?
- `sys.stdin.read()` → **str**(글자) 로 읽는다. 유니코드 해석을 하느라 조금 느리다
- `sys.stdin.buffer.read()` → **bytes**(바이트) 로 읽는다. 해석을 안 해서 더 빠르다

`int()` 는 bytes 도 알아서 숫자로 바꿔줘서 `int(b'42')` 가 그냥 된다.
하지만 **문자열로 써야 할 때는 `.decode()` 가 필요**하다.

```python
int(b'42')            # ✓ 42
b'0100'[0]            # ✗ 48  (문자가 아니라 바이트 숫자가 나온다!)
b'0100'.decode()[0]   # ✓ '0'
```

격자 문제(`0100` 같은 줄)에서 이거 때문에 자주 깨진다. → `data[i].decode()`

---

## 2. `def main():` 으로 감싸는 이유

```python
def main():
    ...
main()
```

장식이 아니라 **속도** 때문이다. 파이썬은 함수 안의 **지역 변수**를 전역 변수보다
훨씬 빠르게 찾는다. 반복이 10만 번 넘어가면 이것만으로 체감이 될 정도로 차이가 난다.

덤으로 `return` 으로 함수를 즉시 빠져나올 수 있다. (전역 코드에서는 `return` 을 못 쓴다)

```python
def main():
    ...
    if 답을_찾음:
        print(answer)
        return        # 여기서 끝. 아래로 안 내려감
    print(-1)
```

---

## 3. 출력 빠르게 하기

`print` 는 호출할 때마다 화면에 내보내려 해서 **호출 횟수 자체가 비싸다.**
답이 여러 줄이면 리스트에 모아서 한 번에 내보낸다.

```python
out = []
for ...:
    out.append(답)
sys.stdout.write("\n".join(map(str, out)) + "\n")
```

- `map(str, out)` — 숫자 리스트를 문자열로 바꾼다 (`join` 은 문자열만 받는다)
- `"\n".join([...])` — 사이사이에 줄바꿈을 끼워 하나의 큰 문자열로

한 줄에 여러 값을 공백으로 출력할 땐 그냥 콤마를 쓰면 된다.

```python
print(a, b)        # "20 2"  — 콤마 자리에 공백이 들어간다
print(*nums)       # 리스트를 풀어서 공백 구분 출력
```

---

## 4. `_` (언더바)

```python
for _ in range(t):
```
특별한 문법이 아니라 **그냥 변수 이름**이다. `for i in range(t)` 와 똑같이 동작한다.
"이 변수는 안 쓸 거예요"라는 관습적 표시일 뿐.

---

## 5. "비어 있는 것은 거짓" (truthy / falsy)

```python
if not stack:      # 스택이 비었으면
while q:           # 큐에 뭔가 있는 동안
```

파이썬은 아래를 전부 **False** 로 친다:
```
0        0.0        ''        []        {}        ()       None
```
그래서 `len(stack) == 0` 대신 `not stack`, `len(q) > 0` 대신 `q` 라고 쓴다.

---

## 6. `and` / `or` 의 단락 평가 (short-circuit) ⭐

**`and` 는 왼쪽이 거짓이면 오른쪽을 실행조차 안 한다.** `or` 는 왼쪽이 참이면 마찬가지.

이게 문법 지식이 아니라 **에러 방지 도구**로 쓰인다.

```python
if 0 <= i < n and arr[i] == x:     # ✓ 범위 확인이 먼저 → 안전
if arr[i] == x and 0 <= i < n:     # ✗ 범위 밖이면 IndexError 로 죽는다
```

```python
if not stack or stack.pop() != PAIR[ch]:   # ✓ 비었으면 pop 을 안 한다
```

**"안전한지 먼저 확인 → 그 다음에 접근"** 순서. 코테에서 무한히 반복되는 패턴이다.

---

## 7. 연쇄 비교

```python
if 0 <= nr < n:
```
`0 <= nr and nr < n` 과 같다. 파이썬에서만 되는 문법이고, 격자 범위 체크에서 늘 쓴다.

---

## 8. 조건부 표현식 (삼항 연산자)

```python
print(best if best <= n else 0)
```
`A if 조건 else B` = 조건이 참이면 A, 아니면 B. 아래와 같다.
```python
if best <= n:
    print(best)
else:
    print(0)
```
`if` 문과 달리 **값을 만들어내는 식**이라서 `print(...)` 안이나 대입문 오른쪽에 바로 쓸 수 있다.

---

## 9. 자주 만나는 에러와 원인

| 에러 | 대표 원인 |
|------|----------|
| `IndexError: list index out of range` | 범위 체크를 배열 접근보다 늦게 함 / 빈 리스트에 `pop()` |
| `TypeError: sequence item 0: expected str instance, int found` | `"\n".join(숫자리스트)` → `map(str, ...)` 빠뜨림 |
| `ValueError: invalid literal for int()` | 입력 토큰을 잘못 세서 엉뚱한 걸 `int()` 함 |
| `RecursionError` | 깊은 재귀 DFS. **BFS(deque)로 바꿔라** |
| `KeyError` | 딕셔너리에 없는 키 조회 → `.get(k, 기본값)` 사용 |
| 답은 맞는데 **시간 초과** | `input()` 반복 / `print` 반복 / 리스트 `.pop(0)` |
