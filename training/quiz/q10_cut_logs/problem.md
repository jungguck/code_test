# Q10. 통나무 자르기 ⭐⭐⭐ (실버 / 파라메트릭 이분탐색)

## 문제
로봇 팔에 절단기가 달려 있다. 절단기의 높이를 `H` 로 맞추고 통나무 N개를 한 번에 자르면,
각 통나무에서 **H를 넘는 부분만** 잘려 나온다.
(길이 `x` 인 통나무는 `x > H` 일 때 `x - H` 만큼, 아니면 0)

잘려 나온 조각들의 **길이 합이 최소 M 이상**이 되게 하면서,
절단기 높이 `H` 를 **최대한 높게** 잡고 싶다. 그 최대 H를 구하라.

## 입력
- 첫째 줄: N, M  (1 ≤ N ≤ 1,000,000 / 1 ≤ M ≤ 2,000,000,000)
- 둘째 줄: N개의 정수 — 통나무 길이  (1 ≤ 길이 ≤ 1,000,000,000)

## 출력
- 최소 M 이상을 얻을 수 있는 절단기 높이 H의 최댓값

## 예제 입력
```
4 7
20 15 10 17
```

## 예제 출력
```
15
```

### 풀이 과정
```
H=15 -> (20-15)+(17-15) = 5+2 = 7  >= 7  OK, 더 높여보자
H=16 -> (20-16)+(17-16) = 4+1 = 5  <  7  모자람
=> 답은 15
```

## 힌트
- H를 0부터 max(길이)까지 하나씩 시도하면 **너무 느리다**(10억)
- **H가 커질수록 얻는 양은 줄어든다** → 단조성이 있으니 **이분탐색**이 가능
- "얻는 양 ≥ M 이면 H를 더 키우고, 모자라면 줄인다" 를 `lo ≤ hi` 로 반복
- 합이 int 범위를 넘을 수 있지만 파이썬 정수는 무한대라 걱정 없다

## 채점
```
python training/quiz/judge.py q10_cut_logs
```

---

## English version

### Q10. Cutting Logs (silver / parametric binary search)

A cutter is set to height `H`. Cutting N logs at once yields, from each log, **only the part
above H** (a log of length `x` gives `x - H` if `x > H`, else 0). You want the **total cut
length to be at least M**, while keeping the cutter height `H` **as high as possible**. Find
that maximum `H`.

**Input** — The first line has N and M (1 ≤ N ≤ 1,000,000; 1 ≤ M ≤ 2,000,000,000). The second
line has N log lengths (1 … 1,000,000,000).

**Output** — The maximum height H that still yields at least M in total.

**Sample Input**
```
4 7
20 15 10 17
```
**Sample Output**
```
15
```

> 단어장: cutter(절단기) / height(높이) / at least(최소, 이상) / as high as possible(가능한 한 높게)
> / monotonic(단조적인) / binary search(이분탐색) / yield(내다, 산출하다)
