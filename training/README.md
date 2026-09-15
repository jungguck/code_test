# 코딩테스트 훈련장 🏋️

mobile_robot_proto_type 코드에서 실제로 쓰는 개념들을 코테 문제로 바꿔놓은 폴더.

## 진행 방식

1. `dayNN_.../problem.md` 읽기
2. `solution.py` 의 `TODO` 부분만 채우기 (함수 시그니처는 건드리지 말 것)
3. 채점:
   ```
   python training/day01_wheel_speed/test_solution.py   # (A모드 폴더는 아직 이 레포에 없음)
   ```
   전부 통과하면 `ALL PASS 🎉` 가 뜬다.
4. 막히면 나한테 "힌트" 라고만 말해도 됨. 답은 안 알려주고 방향만 준다.

## 난이도 표

### A. 함수 채우기형 (로봇 기반)
| 폴더 | 주제 | 난이도 |
|------|------|--------|
| day01_wheel_speed | 차동구동 정/역기구학 | ⭐ (풀이 완료) |

### B. 백준/프로그래머스 스타일 (표준입출력)
| 폴더 | 주제 | 난이도 |
|------|------|--------|
| boj/p01_sort_desc | 정렬 | ⭐ 브론즈 |
| boj/p02_word_count | 해시(dict) | ⭐⭐ 브론즈~실버 |
| boj/p03_bracket | 스택 | ⭐⭐ 실버 |

B는 `solution.py` 가 **표준입력으로 읽고 print 로 출력**하는 형식이다. 채점:
```
python training/boj/judge.py p01_sort_desc   # 한 문제만
python training/boj/judge.py                 # 전체
```


### C. RAW 모드 — 내장 기능 금지 (원리 직접 구현) 🔧
B와 **같은 문제**인데 파이썬이 대신 해주던 걸 직접 만들어야 한다.

| 폴더 | 직접 만들 것 | 원리 |
|------|-------------|------|
| raw/r01_sort | 병합 정렬 | 분할정복, O(n log n) |
| raw/r02_hashmap | 해시 테이블 | 해시 함수 + 체이닝 |
| raw/r03_stack | 배열 기반 스택 | top 인덱스 하나로 LIFO |

```
python training/raw/judge.py r01_sort
python training/raw/judge.py               # 전체
```

RAW 채점기는 3가지를 본다:
1. **[BAN]** — `banned.txt` 의 금지 기능을 쓰면 즉시 탈락 (주석/문자열 안은 봐줌)
2. **[TLE]** — 5초 초과. O(n²)로 짜면 큰 테스트에서 여기 걸린다
3. **[PASS/FAIL]** — 출력 일치 여부

`allowed.txt` 가 있으면 그 표현은 예외 (예: 직접 만든 `stack.pop()` 은 허용, 리스트의 `.pop()` 은 금지).

### D. QUIZ 모드 — 오늘의 랜덤 퀴즈용 문제 세트 🎲
`training/quiz/` — 여러 개를 섞어서 계속 돌려 풀라고 만든 문제들.
각 폴더에 **`problem.md`(한글+English) / `solution.py`(빈칸) / `answer.py`(정답 코드) / `tests/`(예상 입출력)** 이 들어있다.

| 폴더 | 주제 | 핵심 알고리즘 | 난이도 |
|------|------|--------------|--------|
| quiz/q01_battery_log | 배터리 로그 | 시뮬레이션 + 클램핑 | ⭐ 쉬움 (브론즈) |
| quiz/q02_min_window | 최소 이동 구간 | 투 포인터 / 슬라이딩 윈도우 | ⭐⭐⭐ 중간 (실버) |
| quiz/q03_job_schedule | 마감일 스케줄링 | 그리디 + 최소 힙 | ⭐⭐⭐ 중간 (실버~골드) |
| quiz/q04_wall_break | 벽 부수고 이동 | 상태 BFS `visited[r][c][k]` | ⭐⭐⭐⭐ 어려움 (골드) 🔥 |
| quiz/q05_mod_subarray | M의 배수 구간 세기 | 누적합 + 나머지 카운팅 | ⭐⭐⭐⭐ 어려움 (골드) 🔥 |

```
python training/quiz/judge.py q04_wall_break   # 한 문제
python training/quiz/judge.py                  # 전체
python training/quiz/judge.py --answer         # 모범답안으로 채점 (정답 확인용)
```

푸는 순서 추천: **q01 → q02 → q05 → q03 → q04**
(q05는 아이디어만 알면 코드가 10줄이라, 골드지만 q03보다 먼저 뚫린다)

> 막히면 `problem.md` 의 **접근법** 섹션까지만 읽고 `answer.py` 는 보지 말 것.
> 그래도 안 되면 `answer.py` 를 읽고 **닫은 뒤 처음부터 다시 타이핑**해라. 눈으로만 보면 안 남는다.

### 🌐 영어 코딩테스트 대비
`training/ENGLISH.md` — 함수 완성형(LeetCode) 형식, 제약조건 영어 단어표,
지문 상투 표현, 인터뷰 영어 문장. 각 quiz 문제의 `problem.md` 하단에 **English version** 도 붙어있다.

## 규칙
- A/B 모드: 표준 라이브러리 자유롭게
- C(RAW) 모드: `banned.txt` 를 먼저 읽을 것
- D(QUIZ) 모드: `answer.py` 는 최후의 수단. 먼저 `solution.py` 의 TODO 를 채워라

## 다른 컴퓨터에서 이어서 공부하기 💻↔️💻

이 훈련장은 `jungguck/code_test` 레포의 `training/` 폴더에 들어있다.
(레포 루트의 `Python/백준/`, `백준/` 는 BaekjoonHub 확장이 자동으로 올리는 폴더 —
 손대지 말 것. 루트 `README.md` 도 확장이 매번 새로 덮어쓴다.)

### 처음 쓰는 컴퓨터에서
```
git clone https://github.com/jungguck/code_test.git
cd code_test
python training/boj/judge.py       # 바로 채점 가능
```

### 매번 공부 시작할 때
```
git pull
```

### 공부 끝내고 저장할 때
```
git add training
git commit -m "training: p01 풀이"
git push
```

> `git add training` 처럼 **training 폴더만** 스테이징하면
> BaekjoonHub가 올려놓은 파일과 섞이지 않는다.

### pull 이 거부될 때 (다른 컴퓨터에서 이미 push 한 경우)
```
git pull --rebase
```
