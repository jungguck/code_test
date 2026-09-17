# Q09. 구간 에너지 합 ⭐⭐ (실버 / 누적합)

## 문제
로봇의 배터리 셀이 N개 일렬로 있고, 각 셀의 에너지 값이 주어진다.
Q개의 질의가 들어온다. 각 질의는 두 정수 `l r` 로,
**l번째부터 r번째 셀까지의 에너지 합**을 묻는다 (1-indexed, 양 끝 포함).

각 질의의 답을 한 줄씩 출력하라.

## 입력
- 첫째 줄: N, Q  (1 ≤ N, Q ≤ 100,000)
- 둘째 줄: N개의 정수  (-1,000 ≤ 값 ≤ 1,000)
- 다음 Q개의 줄: 각 줄에 `l r`  (1 ≤ l ≤ r ≤ N)

## 출력
- 각 질의의 구간합을 순서대로 한 줄씩

## 예제 입력
```
5 3
1 2 3 4 5
1 5
2 3
3 3
```

## 예제 출력
```
15
5
3
```

## 힌트
- 질의마다 `for` 로 더하면 **O(N·Q)** 라 최악 100억 → 시간 초과
- **누적합(prefix sum)** 을 한 번 만들어 두면 각 질의는 **뺄셈 한 번(O(1))**
- `pre[i]` = 앞에서 i개의 합. 그러면 `[l, r]` 합 = `pre[r] - pre[l-1]`
- 질의가 많으니 `sys.stdin.readline` 으로 입력받는다

## 채점
```
python training/quiz/judge.py q09_range_sum
```

---

## English version

### Q09. Range Energy Sum (silver / prefix sum)

There are **N** battery cells in a row, each with an energy value. **Q** queries follow; each
query `l r` asks for the **sum of energies from cell l to cell r** (1-indexed, inclusive).
Print each answer on its own line.

**Input** — The first line has N and Q (1 ≤ N, Q ≤ 100,000). The second line has N integers
(-1,000 … 1,000). Each of the next Q lines has `l r` (1 ≤ l ≤ r ≤ N).

**Output** — For each query, print the range sum on its own line.

**Sample Input**
```
5 3
1 2 3 4 5
1 5
2 3
3 3
```
**Sample Output**
```
15
5
3
```

> 단어장: prefix sum(누적합) / query(질의) / inclusive(양 끝 포함) / cumulative(누적의)
> / on its own line(각자 한 줄에) / range(구간)
