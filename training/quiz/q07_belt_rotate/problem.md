# Q07. 컨베이어 회전 ⭐⭐ (실버 / 자료구조 deque)

## 문제
컨베이어 벨트 위에 N개의 상자가 왼쪽부터 순서대로 놓여 있다.
로봇이 M개의 명령을 순서대로 수행한다.

- `L k` : 벨트를 **왼쪽으로 k칸** 순환시킨다 (맨 앞 상자들이 뒤로 돌아온다)
- `R k` : 벨트를 **오른쪽으로 k칸** 순환시킨다 (맨 뒤 상자들이 앞으로 돌아온다)

"순환"이므로 끝을 넘어간 상자는 반대편 끝으로 다시 들어온다.
모든 명령이 끝난 뒤 벨트의 상태를 왼쪽부터 출력하라.

## 입력
- 첫째 줄: N, M  (1 ≤ N ≤ 200,000 / 1 ≤ M ≤ 200,000)
- 둘째 줄: N개의 정수 — 벨트 위 상자 값
- 다음 M개의 줄: 각 줄에 명령 하나 (`L k` 또는 `R k`, 0 ≤ k ≤ 10^9)

## 출력
- 최종 벨트 상태를 공백으로 구분해 한 줄에 출력

## 예제 입력
```
5 2
1 2 3 4 5
R 2
L 1
```

## 예제 출력
```
5 1 2 3 4
```

### 풀이 과정
```
시작       1 2 3 4 5
R 2 (오른쪽 2칸)   4 5 1 2 3
L 1 (왼쪽 1칸)     5 1 2 3 4
```

## 힌트
- `k` 가 N보다 클 수 있다. **`k %= n`** 으로 줄여야 10^9 회전도 한 번에 끝난다
- `collections.deque` 의 `rotate()` 를 쓰면 한 줄이다. **오른쪽이 양수, 왼쪽이 음수**
- 직접 슬라이싱으로 풀 수도 있다: `R k` 는 `a[-k:] + a[:-k]`

## 채점
```
python training/quiz/judge.py q07_belt_rotate
```

---

## English version

### Q07. Conveyor Rotation (silver / deque)

There are **N** boxes on a conveyor belt, ordered from the left. A robot performs **M**
commands in order:
- `L k` — rotate the belt **left by k** positions,
- `R k` — rotate the belt **right by k** positions.

The belt is circular, so a box pushed off one end reappears at the other end. After all
commands, print the belt from left to right.

**Input** — The first line has N and M (1 ≤ N, M ≤ 200,000). The second line has N integers.
Each of the next M lines is a command `L k` or `R k` (0 ≤ k ≤ 10^9).

**Output** — Print the final belt, separated by spaces.

**Sample Input**
```
5 2
1 2 3 4 5
R 2
L 1
```
**Sample Output**
```
5 1 2 3 4
```

> 단어장: rotate(회전하다) / circular(순환하는) / position(자리) / reappear(다시 나타나다)
> / modulo(나머지 연산) / to the left/right(왼쪽/오른쪽으로)
