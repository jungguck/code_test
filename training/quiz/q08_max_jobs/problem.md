# Q08. 작업 최대 개수 ⭐⭐⭐ (실버 / 그리디)

## 문제
로봇은 한 번에 **하나의 작업만** 할 수 있다. 작업 N개가 주어지고,
각 작업은 시작 시각 `s` 와 끝 시각 `e` 를 가진다.

한 작업이 끝난 **바로 그 시각에** 다음 작업을 시작할 수 있다 (즉 `e ≤ s'` 이면 이어서 가능).
로봇이 수행할 수 있는 작업의 **최대 개수**를 구하라.

## 입력
- 첫째 줄: N  (1 ≤ N ≤ 100,000)
- 다음 N개의 줄: 각 줄에 `s e`  (0 ≤ s < e ≤ 1,000,000,000)

## 출력
- 겹치지 않게 고를 수 있는 작업의 최대 개수

## 예제 입력
```
5
1 3
3 5
5 7
2 9
0 6
```

## 예제 출력
```
3
```

### 풀이 과정
```
끝나는 시각 기준 정렬: (1,3) (3,5) (0,6) (5,7) (2,9)
(1,3) 선택           끝=3
(3,5) 3>=3 선택      끝=5
(0,6) 0>=5 X
(5,7) 5>=5 선택      끝=7
(2,9) 2>=7 X
=> 3개
```

## 힌트
- **끝나는 시각이 빠른 것부터** 고르는 게 핵심이다 (시작 시각 정렬은 틀린다)
- 정렬 후 한 번 훑으며 "직전에 고른 작업의 끝 ≤ 지금 작업의 시작" 이면 선택
- `jobs.sort(key=lambda x: (x[1], x[0]))` — 끝시각 우선, 같으면 시작시각

## 채점
```
python training/quiz/judge.py q08_max_jobs
```

---

## English version

### Q08. Maximum Number of Jobs (silver / greedy)

The robot can do **only one job at a time**. Each of the N jobs has a start time `s` and an
end time `e`. A job may start exactly when the previous one ends (so `e ≤ s'` means they do
not overlap). Find the **maximum number of jobs** the robot can complete.

**Input** — The first line has N (1 ≤ N ≤ 100,000). Each of the next N lines has `s e`
(0 ≤ s < e ≤ 10^9).

**Output** — The maximum number of non-overlapping jobs.

**Sample Input**
```
5
1 3
3 5
5 7
2 9
0 6
```
**Sample Output**
```
3
```

> 단어장: greedy(그리디, 탐욕적) / overlap(겹치다) / select(고르다) / at a time(한 번에)
> / non-overlapping(겹치지 않는) / sort by(~기준으로 정렬)
