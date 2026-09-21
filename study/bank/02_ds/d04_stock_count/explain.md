# 답지 — D04. 부품 재고

## 핵심 아이디어
**"한 번 세어두고, 조회는 즉시."**

세는 데 O(N) 한 번, 그 뒤로는 몇 번을 물어보든 한 번에 O(1) 로 답한다.

## dict 가 왜 빠른가
리스트에서 `parts.count("bolt")` 는 **처음부터 끝까지 전부 훑는다.** O(N).
dict 는 이름을 숫자로 바꿔서(해시) **그 숫자를 배열 위치로 바로 써버린다.** 훑을 필요가 없다. O(1).

```
"bolt"  --해시함수-->  3901  -->  table[3901] 을 바로 본다
```

## 코드가 하는 일
```python
stock = {}
for name in parts:
    stock[name] = stock.get(name, 0) + 1
```
`stock.get(name, 0)` 은 **"있으면 그 값, 없으면 0"** 이다.
처음 보는 이름이면 0 + 1 = 1, 이미 있으면 기존값 + 1.

## 초보가 막히는 곳

**① `stock[name] + 1` 로 쓰면 에러**
```python
stock[name] = stock[name] + 1     # ❌ 없는 키를 읽으면 KeyError
stock[name] = stock.get(name, 0) + 1   # ✅ 없으면 0으로 쳐준다
```

**② 더 짧게 쓰는 법 (알아두면 편함)**
```python
from collections import Counter
stock = Counter(parts)            # 한 줄로 개수를 다 세준다
```
`Counter` 는 없는 키를 물어봐도 에러 없이 0을 준다. 실전에선 이걸 쓰면 된다.
여기서는 **원리를 보려고** 일부러 dict 로 직접 썼다.

**③ `input()` 을 그냥 호출한 줄은 뭔가?**
```python
input()                # N 값을 읽긴 읽는데 아무 데도 안 쓴다
parts = input().split()
```
N은 부품 개수인데, `split()` 이 알아서 전부 쪼개주므로 개수를 알 필요가 없다.
하지만 **입력 줄은 순서대로 읽어야 하므로** 건너뛰려면 한 번 읽어서 버려야 한다.

**④ `[... for name in queries]` (리스트 컴프리헨션)**
```python
answer = [stock.get(name, 0) for name in queries]
```
풀어 쓰면 이것과 같다:
```python
answer = []
for name in queries:
    answer.append(stock.get(name, 0))
```

## 시간복잡도
O(N + M) — 세는 데 N번, 물어보는 데 M번.
