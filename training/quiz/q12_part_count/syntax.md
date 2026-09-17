# Q12 파이썬 문법 노트 🐍

> 공통 문법(`input()`, `map`, 출력)은 [`SYNTAX.md`](../SYNTAX.md) 참고.

## 이 문제에 나오는 문법

### 1. `collections.Counter` — 개수 세기 한 줄

```python
from collections import Counter
names = [input() for _ in range(n)]
cnt = Counter(names)
```

넣어준 값들의 **등장 횟수를 자동으로 세어** dict 처럼 만들어 준다.
`cnt["motor"]` 로 횟수를 꺼낸다. 직접 세면 이렇게 되는 걸 대신해 준다.

```python
cnt = {}
for name in names:
    cnt[name] = cnt.get(name, 0) + 1     # 없으면 0에서 시작해 +1
```

### 2. 리스트를 만들 필요도 없다 (참고)

```python
cnt = Counter(input() for _ in range(n))
```

`[ ... ]` 대신 괄호 없이 넘기면 **제너레이터** — 리스트를 안 만들고 `input()` 을
N번 흘려보낸다. `Counter` 가 하나씩 받아 세므로 이렇게도 된다.
(단, 나중에 원본 목록이 또 필요하면 위처럼 `names` 리스트로 받아두는 게 편하다)

### 3. 동률 규칙을 "자명한 세 줄" 로 풀기

```python
best = max(cnt.values())                          # 가장 많은 횟수
winners = [name for name in cnt if cnt[name] == best]   # 그 횟수인 이름들
print(min(winners), best)                         # 사전순 앞선 이름
```

한 줄씩 뜻이 그대로 읽힌다.
- `cnt.values()` : 횟수들 → 그 중 최댓값이 `best`
- `winners` : **best 와 같은 횟수**를 가진 이름만 모은다 (동률 후보)
- `min(winners)` : 문자열의 `min` 은 **사전순으로 가장 앞선 것**

> 💡 `min(cnt, key=lambda x: (-cnt[x], x))` 처럼 **부호를 뒤집어 한 줄로** 푸는 방법도 있다.
> 짧지만 "왜 마이너스?"에서 막히기 쉬워서, 학습용에선 위처럼 **풀어 쓰는 걸 권한다.**
> 코드가 짧은 게 목표가 아니라 읽고 이해하는 게 목표다.

### 4. `print(name, best)` — 값 두 개 출력

```python
print(min(winners), best)       # "gear 2"
```

`print` 가 사이에 공백을 넣어 준다. ([SYNTAX.md 3번](../SYNTAX.md))

## 정렬로 풀어도 된다

```python
items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
print(items[0][0], items[0][1])
```

`cnt.items()` 는 `(이름, 횟수)` 쌍들. `(-횟수, 이름)` 기준으로 정렬한 뒤 맨 앞을 쓴다.
상위 몇 개가 필요하면 이 방식이 편하다.
