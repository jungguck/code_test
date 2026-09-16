# Q01 파이썬 문법 노트 🐍

> 공통 문법(`input = sys.stdin.readline`, `map`, 출력)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. 한 줄에서 두 값 받기

```python
n, b = map(int, input().split())
```

입력 `5 50` 이 `n = 5`, `b = 50` 으로 나뉘어 들어간다.
변수 개수와 값 개수가 **정확히 맞아야** 한다. (자세한 건 [SYNTAX.md 2번](../SYNTAX.md))

### 2. `+=` (복합 대입 연산자)

```python
b += d             # b = b + d 와 같다
empty += 1         # empty = empty + 1
```
`-=`, `*=`, `//=` 도 같은 식으로 쓴다. 변수 이름을 두 번 안 써서 오타가 줄어든다.

### 3. `if / elif` 로 값 자르기 (clamp)

```python
if b < 0:
    b = 0
elif b > 100:
    b = 100
```

`elif` 는 **앞의 `if` 가 거짓일 때만** 검사한다.
여기선 `b` 가 0보다 작으면서 동시에 100보다 클 수는 없으니 `elif` 가 맞다.
(`if` 두 개로 써도 결과는 같지만 쓸데없이 한 번 더 비교한다)

한 줄로 줄이는 관용구도 있다. 익숙해지면 이쪽이 더 많이 보인다.
```python
b = max(0, min(100, b))
```
안쪽 `min(100, b)` 가 위를 자르고, 바깥 `max(0, ...)` 가 아래를 자른다.

### 4. `print(a, b)` — 콤마로 여러 값 출력

```python
print(b, empty)     # "20 2"
```
`print` 는 인자 사이에 **자동으로 공백 하나**를 넣는다.
`print(str(b) + " " + str(empty))` 처럼 쓸 필요가 없다.

바꾸고 싶으면:
```python
print(a, b, sep=',')     # "20,2"
print(a, end='')         # 줄바꿈 없이
```

### 5. `for d in ds:` — 인덱스 없이 원소를 바로 꺼내기

```python
for d in ds:
    b += d
```

`for i in range(len(ds)): b += ds[i]` 와 결과는 같지만, **인덱스가 필요 없으면**
원소를 바로 꺼내는 쪽이 짧고 실수가 적다.

인덱스도 같이 필요하면 `enumerate` 를 쓴다.
```python
for i, d in enumerate(ds):      # i = 0, 1, 2 ... / d = 원소
    ...
```

## 이 문제에서 실수하기 쉬운 곳

```python
b += d
if b == 0:          # ✗ 자르기 전에 확인 → b 가 -40 이면 0이 아니라서 못 센다
    empty += 1
if b < 0:
    b = 0
```
**자른 다음에** 0인지 봐야 한다. 순서가 곧 정답이다.
