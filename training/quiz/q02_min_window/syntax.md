# Q02 파이썬 문법 노트 🐍

> 공통 문법(입력 읽기, `map`, 출력)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. `list(map(int, ...))` — 한 번에 형 변환

```python
a = list(map(int, input().split()))
```

`map(함수, 반복가능한것)` 은 **원소 하나하나에 함수를 적용**한다.

```python
list(map(int, ['3', '1', '4']))    # → [3, 1, 4]
```

`map` 자체는 리스트가 아니라 **게으른 반복자**(lazy iterator)라서 `list()` 로 감싸야
진짜 리스트가 된다.

```python
m = map(int, ['1', '2'])
m[0]           # ✗ TypeError — 인덱스 접근 불가
list(m)[0]     # ✓ 1
```

**한 번만 훑고 버릴 거면** `list()` 없이 써도 된다(메모리 절약). 하지만 이 문제는
`a[right]`, `a[left]` 로 **인덱스 접근**을 해야 하므로 반드시 `list()` 로 감싼다.

같은 걸 리스트 컴프리헨션으로 쓰면:
```python
a = [int(x) for x in input().split()]     # 결과 동일. map 이 조금 더 빠르다
```

### 2. 두 포인터를 다루는 `for` + `while` 중첩

```python
for right in range(n):
    total += a[right]
    while total >= s:
        ...
        left += 1
```

**중첩이지만 O(N²)가 아니다.** 안쪽 `while` 이 도는 횟수는 `left` 가 전진한 횟수인데,
`left` 는 0에서 n까지 **한 방향으로만** 간다. 그래서 전체 합쳐도 n번.

이걸 헷갈리지 않으려면 "안쪽 루프가 몇 번 도나"가 아니라
**"이 변수가 평생 몇 칸 움직이나"** 를 세면 된다.

```python
if total >= s:      # ✗ 한 번만 줄인다 → 더 짧은 답을 놓친다
while total >= s:   # ✓ 줄일 수 있는 만큼 계속 줄인다
```

### 3. "불가능"을 나타내는 초깃값 (sentinel)

```python
best = n + 1        # 있을 수 없는 값
...
if best <= n:
    print(best)
else:
    print(0)
```

구간 길이는 아무리 길어도 `n` 이다. 그래서 `n + 1` 은 **절대 나올 수 없는 값**이고,
끝까지 `n + 1` 이면 "한 번도 갱신 안 됐다" 는 뜻이 된다.

`float('inf')` (무한대) 를 써도 된다.
```python
best = float('inf')
...
if best == float('inf'):
    print(0)
else:
    print(best)
```
정수와 비교도 되고 어떤 정수보다도 크다. 다만 최종 출력 전에 **반드시 걸러내야** 한다.
그대로 출력하면 `inf` 라고 찍힌다.

### 4. 길이에 이름을 붙여서 갱신하기

```python
length = right - left + 1

if length < best:
    best = length
```

`best = min(best, right - left + 1)` 한 줄로 써도 결과는 똑같다.
그런데 `length` 라는 **이름을 붙여 놓으면** "지금 창의 길이" 라는 게 바로 보이고,
같은 식을 두 번 쓰지 않아도 된다.

```python
# 같은 뜻. 익숙해지면 이렇게 써도 된다
best = min(best, right - left + 1)
```

`min()` 은 함수 호출이라 아주 조금 느리지만, 이 정도는 신경 쓸 수준이 아니다.
**읽기 쉬운 쪽을 고르면 된다.**

### 5. 구간 길이 공식 `right - left + 1`

```
인덱스:  0  1  2  3  4
              ↑     ↑
            left   right       길이 = 4 - 2 + 1 = 3
```
**`+1` 을 빼먹는 게 코테 최다 실수 중 하나다.** 양 끝을 모두 포함하니까 1을 더한다.
헷갈리면 `left == right` 인 경우를 넣어보면 된다 → 길이 1이 나와야 정상.
