# Q12. 부품 개수 세기 ⭐⭐ (브론즈~실버 / 해시)

## 문제
조립 라인에서 N개의 부품이 지나갔고, 각 부품의 **이름**(공백 없는 문자열)이 순서대로 주어진다.

가장 많이 지나간 부품의 **이름과 그 횟수**를 출력하라.
가장 많이 지나간 부품이 여러 개면 **사전순으로 가장 앞선 이름**을 답으로 한다.

## 입력
- 첫째 줄: N  (1 ≤ N ≤ 100,000)
- 다음 N개의 줄: 각 줄에 부품 이름 하나 (알파벳 소문자, 길이 1~20)

## 출력
- `이름 횟수` 를 공백으로 구분해 한 줄에 출력

## 예제 입력
```
5
motor
gear
motor
sensor
gear
```

## 예제 출력
```
gear 2
```

### 풀이 과정
```
motor 2, gear 2, sensor 1
최다 = 2  (motor, gear 동률)
사전순 앞선 것 = gear
=> gear 2
```

## 힌트
- 이름 → 횟수를 `dict` 로 세거나 `collections.Counter` 한 줄로 센다
- 동률 처리가 핵심: **횟수는 많을수록, 이름은 사전순 앞설수록** 우선
- `min(c, key=lambda x: (-c[x], x))` — 횟수에 마이너스를 붙여 "많은 게 먼저"

## 채점
```
python training/quiz/judge.py q12_part_count
```

---

## English version

### Q12. Counting Parts (bronze–silver / hashing)

On an assembly line, **N** parts passed by; the **name** of each part (a string without spaces)
is given in order. Print the **name and count** of the most frequent part. If several parts tie
for the most, print the **lexicographically smallest** name.

**Input** — The first line has N (1 ≤ N ≤ 100,000). Each of the next N lines has one part name
(lowercase letters, length 1–20).

**Output** — Print `name count`, separated by a space.

**Sample Input**
```
5
motor
gear
motor
sensor
gear
```
**Sample Output**
```
gear 2
```

> 단어장: frequency(빈도) / count(개수를 세다) / tie(동률) / lexicographically(사전순으로)
> / assembly line(조립 라인) / most frequent(가장 빈번한)
