# 코딩테스트 훈련장 🏋️

mobile_robot_proto_type 코드에서 실제로 쓰는 개념들을 코테 문제로 바꿔놓은 폴더.

## 진행 방식

1. `dayNN_.../problem.md` 읽기
2. `solution.py` 를 열기 **전에** 직접 풀어보기 (이제 정답 코드가 들어있다)
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

### D. QUIZ 모드 — 랜덤 퀴즈용 문제 세트 🎲
`training/quiz/` — 여러 개를 섞어서 계속 돌려 풀라고 만든 문제들.
각 폴더 구성:
| 파일 | 내용 |
|------|------|
| `problem.md` | 문제 지문(한글+English) + 접근법 + 함정 |
| `solution.py` | 정답 코드 (주석 포함) |
| `syntax.md` | **그 문제에 쓰인 파이썬 문법 해설** 🐍 |
| `tests/` | 예상 입출력 |

문제는 `problem.md` 만 보고 직접 풀고, 막히면 `solution.py` 를 열어 답을 확인하는 방식.
코드는 이해했는데 **문법이 안 읽히면 `syntax.md`** 를 본다.
(`quiz/SYNTAX.md` = 모든 문제 공통 문법 / 각 폴더 `syntax.md` = 그 문제에만 나오는 문법)

> 다른 AI(Qwen 등)한테 이 문제를 시킬 땐 **폴더를 통째로** 주면 된다.
> `problem.md` + `solution.py` + `syntax.md` 세 개만 있으면 문맥이 전부 들어간다.

| 폴더 | 주제 | 핵심 알고리즘 | 난이도 |
|------|------|--------------|--------|
| quiz/q01_battery_log | 배터리 로그 | 시뮬레이션 + 클램핑 | ⭐ 쉬움 (브론즈) |
| quiz/q02_min_window | 최소 이동 구간 | 투 포인터 / 슬라이딩 윈도우 | ⭐⭐⭐ 중간 (실버) |
| quiz/q03_job_schedule | 마감일 스케줄링 | 그리디 + 최소 힙 | ⭐⭐⭐ 중간 (실버) |
| quiz/q04_clean_zone | 청소 구역 나누기 | BFS 연결 요소 | ⭐⭐⭐ 중간 (실버) |
| quiz/q05_no_overheat | 과열 없이 작업하기 | 1차원 DP (점화식) | ⭐⭐⭐ 중간 (실버) |
| quiz/q06_range_count | 구간 안의 값 개수 | 정렬 + 이분탐색 | ⭐⭐⭐ 중간 (실버) |

이 6개가 **코테 빈출 패턴 5개**를 하나씩 담고 있다 (`ENGLISH.md` 4번 항목 참고):
해시/누적합 · 투 포인터 · 힙 · 그래프 탐색 · DP · 이분탐색.

```
python training/quiz/judge.py q04_clean_zone   # 한 문제
python training/quiz/judge.py                  # 전체
```

푸는 순서 추천: **q01 → q02 → q05 → q06 → q04 → q03**
(q05 DP와 q06 이분탐색은 코드가 10줄 안쪽이라 먼저 뚫린다. q03 힙이 제일 까다롭다)

#### 🔒 보너스 — 나중에 도전 (골드, 지금은 건너뛸 것)
| 폴더 | 주제 | 핵심 알고리즘 |
|------|------|--------------|
| quiz/hard01_wall_break | 벽 부수고 이동 | 상태 BFS `visited[r][c][k]` |
| quiz/hard02_mod_subarray | M의 배수 구간 세기 | 누적합 + 나머지 카운팅 |

위 6개를 다 풀고 나서 보면 훨씬 쉽게 읽힌다.
(hard01은 q04의 BFS에 차원 하나를 더한 것, hard02는 q06처럼 "미리 계산해두고 뺄셈"하는 발상)

### 🌐 영어 코딩테스트 대비
`training/ENGLISH.md` — 함수 완성형(LeetCode) 형식, 제약조건 영어 단어표,
지문 상투 표현, 인터뷰 영어 문장. 각 quiz 문제의 `problem.md` 하단에 **English version** 도 붙어있다.

### 🔍 코드 문법이 이해 안 될 때
`/explain` — 코드를 **문법 위주로, 초보자한테 설명하듯** 해설해주는 슬래시 커맨드.
(정의: `.claude/commands/explain.md`)

```
/explain                                        # IDE에서 열어둔/선택한 코드
/explain training/boj/p03_bracket/solution.py   # 파일 지정
```
알고리즘이 아니라 **파이썬 문법**을 설명한다. 틀린 버전 비교 + 실행 추적 표까지 나온다.

## 규칙
- A/B 모드: 표준 라이브러리 자유롭게
- C(RAW) 모드: `banned.txt` 를 먼저 읽을 것
- D(QUIZ) 모드: `problem.md` 의 **접근법** 섹션까지만 읽고 직접 짜볼 것.
  `solution.py` 를 봤으면 **닫고 처음부터 다시 타이핑**해라. 눈으로만 보면 안 남는다

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
