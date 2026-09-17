# Q11. 세 부품 고르기 ⭐⭐ (브론즈~실버 / 브루트포스)

## 문제
창고에 N개의 부품이 있고 각 부품에는 무게가 적혀 있다.
로봇 팔은 서로 다른 **부품 3개**를 집어 올린다.

세 부품 무게의 합이 **M을 넘지 않으면서(≤ M) 최대**가 되도록 고르고,
그때의 합을 출력하라. (항상 M 이하가 되는 조합이 하나 이상 존재한다)

## 입력
- 첫째 줄: N, M  (3 ≤ N ≤ 100 / 10 ≤ M ≤ 300,000)
- 둘째 줄: N개의 정수 — 부품 무게  (1 ≤ 무게 ≤ 100,000)

## 출력
- 3개를 골라 만들 수 있는, M 이하인 합의 최댓값

## 예제 입력
```
5 21
5 6 7 8 9
```

## 예제 출력
```
21
```

### 풀이 과정
```
5+7+9 = 21  <= 21   <- 최대
5+8+9 = 22  > 21    (탈락)
6+7+8 = 21          (같지만 더 크진 않음)
=> 21
```

## 힌트
- N이 최대 100이라 **3개 조합은 약 16만 개** → 전부 시도해도 된다(브루트포스)
- `itertools.combinations(a, 3)` 이 서로 다른 3개 조합을 모두 만들어 준다
- 삼중 `for i < j < k` 로 직접 돌려도 된다
- 합이 M 이하이면서 지금까지 최댓값보다 크면 갱신

## 채점
```
python training/quiz/judge.py q11_pick_three
```

---

## English version

### Q11. Pick Three Parts (bronze–silver / brute force)

A warehouse has **N** parts, each with a weight. The robot arm picks **three distinct parts**.
Choose them so that the sum of the three weights is **as large as possible without exceeding
M** (≤ M), and print that sum. (At least one valid triple ≤ M always exists.)

**Input** — The first line has N and M (3 ≤ N ≤ 100; 10 ≤ M ≤ 300,000). The second line has N
weights (1 … 100,000).

**Output** — The maximum sum of three parts that does not exceed M.

**Sample Input**
```
5 21
5 6 7 8 9
```
**Sample Output**
```
21
```

> 단어장: distinct(서로 다른) / exceed(초과하다) / combination(조합) / brute force(완전탐색)
> / as large as possible(가능한 한 크게) / triple(세 개 묶음)
