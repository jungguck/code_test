# [Bronze III] 최소, 최대 - 10818 

[문제 링크](https://www.acmicpc.net/problem/10818) 

### 성능 요약

메모리: 128172 KB, 시간: 472 ms

### 분류

수학, 구현

### 제출 일자

2026년 3월 16일 12:26:01

### 문제 설명

<p>N개의 정수가 주어진다. 이때, 최솟값과 최댓값을 구하는 프로그램을 작성하시오.</p>

### 입력 

 <p>첫째 줄에 정수의 개수 N (1 ≤ N ≤ 1,000,000)이 주어진다. 둘째 줄에는 N개의 정수를 공백으로 구분해서 주어진다. 모든 정수는 -1,000,000보다 크거나 같고, 1,000,000보다 작거나 같은 정수이다.</p>

### 출력 

 <p>첫째 줄에 주어진 정수 N개의 최솟값과 최댓값을 공백으로 구분해 출력한다.</p>

### 핵심 차이# Python `map()` vs `list(map())`

### 1. 핵심 차이

| 코드 | 자료형 | 특징 |
|-----|-----|-----|
| `map(int, ...)` | `map` (iterator) | 값을 저장하지 않고 필요할 때 생성 |
| `list(map(int, ...))` | `list` | 모든 값을 리스트에 저장 |

---

### 2. 인덱스 접근

#### map

불가능

```python
num = map(int, input().split())
num[0]  # 오류 발생
```

이유

- `map` 객체는 **iterator**
- 인덱스 접근을 지원하지 않음

---

#### list

가능

```python
num = list(map(int, input().split()))
num[0]  # 정상 작동
```

이유

- `list`는 **인덱스 기반 자료구조**

---

### 3. 입력 처리 과정

```python
input().split()
```

결과

```python
['1', '2', '3']
```

자료형

```
list[str]
```

---

#### map 적용

```python
map(int, input().split())
```

동작

```
int('1')
int('2')
int('3')
```

자료형

```
map (iterator)
```

---

#### 리스트 생성

```python
list(map(int, input().split()))
```

결과

```python
[1, 2, 3]
```

자료형

```
list[int]
```

---

### 4. 알고리즘 문제에서 주로 사용하는 방식

```python
nums = list(map(int, input().split()))
```

이유

1. 인덱스 접근 가능
2. 여러 번 사용 가능
3. 길이 확인 가능 (`len(nums)`)

---

### 5. 요약

```
input().split()
→ 문자열 리스트 생성

map(int, iterable)
→ 각 요소에 int 적용하는 iterator 생성

list(map(int, iterable))
→ iterator 결과를 리스트로 저장
```
코드	자료형	특징
map(int, ...)	map(iterator)	값 저장 안함
list(map(...))	list	값 저장

인덱스 접근
map

불가능

num = map(int,input().split())
num[0]   # 오류
list

가능

num = list(map(int,input().split()))
num[0]   # 가능
