# Q01. 배터리 로그 ⭐ (브론즈 / 시뮬레이션)

## 문제
로봇이 N번 동작한다. i번째 동작에서 배터리가 `d_i` 만큼 변한다.
(`d_i` 가 음수면 방전, 양수면 충전)

배터리는 **항상 0 이상 100 이하**다.
- 계산 결과가 0보다 작아지면 **0으로 잘린다**
- 100보다 커지면 **100으로 잘린다**

N번의 동작이 모두 끝난 뒤,
1. **최종 배터리 값**
2. **동작 직후 배터리가 정확히 0이었던 횟수** (연속으로 0이어도 매번 센다)

를 구하라.

## 입력
- 첫째 줄: N, B  (1 ≤ N ≤ 100,000 / 0 ≤ B ≤ 100) — 동작 횟수와 시작 배터리
- 둘째 줄: N개의 정수 `d_1 ... d_N`  (-100 ≤ d_i ≤ 100)

## 출력
- 최종 배터리와 방전 횟수를 공백으로 구분해 한 줄에 출력

## 예제 입력
```
5 50
-30 -40 60 -100 20
```

## 예제 출력
```
20 2
```

### 풀이 과정
```
시작 50
50 + (-30) =  20        ->  20
20 + (-40) = -20 -> 0   ->   0   (방전 1회)
 0 +   60  =  60        ->  60
60 + (-100)= -40 -> 0   ->   0   (방전 2회)
 0 +   20  =  20        ->  20
최종 20, 방전 2회
```

## 힌트
- `b = max(0, min(100, b + d))` 한 줄이면 위아래 둘 다 잘린다
- 자른 **뒤에** 0인지 확인해야 한다. 자르기 전 `-40` 을 보고 세면 안 된다

## 채점
```
python training/quiz/judge.py q01_battery_log
```

---

## English version

### Q01. Battery Log (easy / simulation)

A robot performs **N** actions. The i-th action changes the battery level by `d_i`
(negative = discharge, positive = charge).

The battery level is **clamped to the range [0, 100]**: anything below 0 becomes 0,
anything above 100 becomes 100.

After all N actions, print:
1. the **final battery level**, and
2. how many times the battery was **exactly 0 right after an action**
   (count every such action, even consecutive ones).

**Input** — The first line contains two integers N and B (1 ≤ N ≤ 100,000; 0 ≤ B ≤ 100),
the number of actions and the initial battery level. The second line contains N integers
`d_1 ... d_N` (-100 ≤ d_i ≤ 100).

**Output** — Print the final battery level and the number of depletions, separated by a space.

**Sample Input**
```
5 50
-30 -40 60 -100 20
```
**Sample Output**
```
20 2
```

> 단어장: clamp(잘라 맞추다) / exceed(초과하다) / at most(최대) / at least(최소)
> / respectively(각각) / separated by a space(공백으로 구분된)
