# Q12 파이썬 문법 노트 🐍

> 공통 문법(`input()`, `map`, 출력)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. `collections.Counter` — 개수 세기 한 줄

```python
from collections import Counter
c = Counter(input() for _ in range(n))
```

넣어준 값들의 **등장 횟수를 자동으로 세어** dict 처럼 만들어 준다.
`c["motor"]` 로 횟수를 꺼낸다. 직접 세면 이렇게 되는 걸 대신해 준다.

```python
c = {}
for _ in range(n):
    name = input()
    c[name] = c.get(name, 0) + 1        # 없으면 0에서 시작해 +1
```

### 2. 제너레이터를 `Counter` 에 바로 넘기기

```python
Counter(input() for _ in range(n))
```

`[ ... ]` 리스트를 안 만들고 `input()` 을 N번 흘려보낸다.
`Counter` 가 하나씩 받아 세므로 리스트를 따로 만들 필요가 없다.

### 3. `min(..., key=...)` 로 동률 규칙 태우기

```python
name = min(c, key=lambda x: (-c[x], x))
```

- `for x in c` : dict 를 돌면 **키(이름)** 가 나온다
- `key` 가 반환하는 튜플 `(-c[x], x)` 로 비교한다
- `-c[x]` : 횟수에 마이너스 → **횟수가 많을수록 값이 작아짐** → `min` 이 고름
- `x` : 횟수가 같으면 **이름이 사전순 앞선 것**이 더 작음 → 그게 뽑힘

**"1순위는 크게, 2순위는 작게"** 를 한 줄로 표현하는 관용구다.
큰 걸 우선하고 싶은 항목에만 마이너스를 붙이는 게 요령이다.

### 4. `print(name, c[name])` — 값 두 개 출력

```python
print(name, c[name])       # "gear 2"
```

`print` 가 사이에 공백을 넣어 준다. ([SYNTAX.md 3번](../SYNTAX.md))

## 정렬로 풀어도 된다

```python
items = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
print(items[0][0], items[0][1])
```

`c.items()` 는 `(이름, 횟수)` 쌍들. 같은 기준 `(-횟수, 이름)` 으로 정렬한 뒤 맨 앞을 쓴다.
`min` 버전이 더 짧지만, 상위 몇 개가 필요하면 `sorted` 가 편하다.
