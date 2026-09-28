# -*- coding: utf-8 -*-
"""내 백준 풀이의 입력 처리 스타일을 검사하고, --fix 로 고친다.

    python study/check_style.py              검사만 (아무것도 안 바꾼다)
    python study/check_style.py --fix        고치고, 저장된 테스트로 출력이 안 바뀐 것만 채택
    python study/check_style.py --test       저장된 테스트만 돌려본다

무엇을 검사하나 — 실제로 내 코드에 있었던 것만 규칙으로 넣었다(2026-09-28 전수조사).

    E1 preamble-missing   input( 을 쓰는데 `input = sys.stdin.readline` 이 없다
    E2 raw-line-no-rstrip `x = input()` 로 줄을 문자열째 받는다 → readline 이면 '\\n' 이 붙는다
    E3 import-sys-missing `input = sys.stdin.readline` 인데 `import sys` 가 없다
    E4 input-prompt       `input("...")` — readline 은 인자를 안 받는다(TypeError)
    W1 range-from-1       `for _ in range(1, ...)` — 변수를 안 쓰는데 1부터 (잡음)

★ E2 가 제일 중요하다. E1 만 고치고 E2 를 놔두면 **멀쩡했던 코드가 조용히 틀린다.**
  실측: 1259(팰린드롬수)는 `n == '0'` 이 `'0\\n'` 과 안 맞아 **무한루프**가 되고,
       16172 는 `K in S` 가 어긋나고, 15829 는 `ord('\\n')-96 = -86` 이 합에 섞인다.
  그래서 --fix 는 E1·E2·E3 를 **같이** 고친다. 하나만 고치는 선택지를 두지 않는다.

★ study/ref/ 는 건드리지 않는다 — 공유받아 검증된 코드다(260921-하네스스킬.md).

안전장치: --fix 는 고치기 **전** 출력을 먼저 기록하고, 고친 **뒤** 다시 돌려
  한 글자라도 달라지면 그 파일을 되돌린다. 저장된 정답(output*.txt)과 비교하는 게
  아니라 **바꾸기 전 내 출력**과 비교한다 — 저장된 정답이 절대 기준이 아니기 때문이다
  (1546 평균: 내 출력 66.66666666666667 / 저장본 66.666667. BOJ 는 오차를 허용한다).
"""
import io
import os
import re
import subprocess
import sys
import glob

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SOLUTION_ROOT = os.path.join(REPO, "Python")     # 내 풀이만. ref/ 는 제외한다.

PREAMBLE = "import sys\ninput = sys.stdin.readline\n"

# `x = input()` — 줄을 문자열째 받는 자리. int(input()) 은 여기 안 걸린다(안쪽이라).
RAW_LINE = re.compile(r"^([ \t]*)([A-Za-z_]\w*)[ \t]*=[ \t]*input\(\)[ \t]*$", re.M)
PROMPT_INPUT = re.compile(r"input\([ \t]*['\"]")
RANGE_FROM_1 = re.compile(r"for[ \t]+_[ \t]+in[ \t]+range\([ \t]*1[ \t]*,")


def solution_files():
    """내 풀이 .py 전부. 문제 폴더 1개에 여러 개면 전부 본다."""
    out = []
    for d in sorted(glob.glob(os.path.join(SOLUTION_ROOT, "*", "*", "*"))):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".py"):
                out.append(os.path.join(d, f))
    return out


def testcases(d):
    """그 폴더의 (입력, 정답) 쌍. input.txt/output.txt 와 input1.txt/output1.txt 둘 다 쓴다."""
    pairs = []
    for ip in sorted(glob.glob(os.path.join(d, "input*.txt"))):
        n = re.sub(r"\D", "", os.path.basename(ip))       # 없으면 "" (번호 없는 형식)
        op = os.path.join(d, "output" + n + ".txt")
        if os.path.exists(op):
            pairs.append((ip, op))
    return pairs


def run(py, ip, timeout=10):
    """풀이 1회 실행 -> (성공?, 출력토큰, 사유). 예외를 위로 던지지 않는다."""
    try:
        with io.open(ip, "rb") as f:
            r = subprocess.run([sys.executable, py], stdin=f,
                               capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, [], "TIMEOUT"
    if r.returncode != 0:
        err = r.stderr.decode("utf-8", "replace").strip().splitlines()
        return False, [], (err[-1] if err else "exit != 0")
    return True, r.stdout.decode("utf-8", "replace").split(), ""


def outputs_of(py):
    """그 풀이의 모든 테스트 출력을 모은다. 실행 실패도 사유째로 기록해 비교 대상에 넣는다."""
    d = os.path.dirname(py)
    res = []
    for ip, _op in testcases(d):
        ok, got, why = run(py, ip)
        res.append((os.path.basename(ip), ok, got, why))
    return res


def check(src):
    """소스 1개 -> 위반 코드 목록."""
    bad = []
    uses_input = "input(" in src
    has_pre = re.search(r"^[ \t]*input[ \t]*=[ \t]*sys\.stdin\.readline", src, re.M)
    if uses_input and not has_pre:
        bad.append("E1")
    if RAW_LINE.search(src):
        bad.append("E2")
    if has_pre and not re.search(r"^[ \t]*import[ \t]+sys\b", src, re.M):
        bad.append("E3")
    if PROMPT_INPUT.search(src):
        bad.append("E4")
    if RANGE_FROM_1.search(src):
        bad.append("W1")
    return bad


def fix(src):
    """E1·E2·E3 를 고친 소스를 돌려준다. E4·W1 은 사람이 봐야 하므로 손대지 않는다."""
    # E2 먼저: 줄을 문자열째 받는 자리에 .rstrip() 을 붙인다.
    #   먼저 해야 하는 이유 — preamble 을 넣은 뒤에 붙이면 그 사이 상태가 '깨진 코드' 다.
    src = RAW_LINE.sub(lambda m: f"{m.group(1)}{m.group(2)} = input().rstrip()", src)

    has_pre = re.search(r"^[ \t]*input[ \t]*=[ \t]*sys\.stdin\.readline", src, re.M)
    has_sys = re.search(r"^[ \t]*import[ \t]+sys\b", src, re.M)
    if "input(" in src and not has_pre:
        src = PREAMBLE + src if src.startswith("#") is False else _insert_after_header(src)
    elif has_pre and not has_sys:
        src = "import sys\n" + src
    return src


def _insert_after_header(src):
    """맨 위 주석(인코딩 선언 등) 아래에 preamble 을 넣는다."""
    lines = src.splitlines(True)
    i = 0
    while i < len(lines) and (lines[i].startswith("#") or not lines[i].strip()):
        i += 1
    return "".join(lines[:i]) + PREAMBLE + "".join(lines[i:])


def read_src(py):
    """소스와 **원래 줄바꿈**을 함께 돌려준다.

    이 저장소는 CRLF 로 커밋돼 있다. LF 로 써버리면 두 줄 고친 게 전체 줄 교체로 잡혀
    diff 를 읽을 수 없게 된다(실측: 31파일 414+/352-). 원래 줄바꿈을 그대로 유지한다.
    """
    raw = io.open(py, "rb").read()
    nl = "\r\n" if raw.count(b"\r\n") else "\n"
    return raw.decode("utf-8", "replace").replace("\r\n", "\n"), nl


def write_src(py, src, nl):
    with io.open(py, "w", encoding="utf-8", newline=nl) as f:
        f.write(src)


def rel(p):
    return os.path.relpath(p, REPO).replace(os.sep, "/")


def cmd_check(files):
    tally = {}
    for py in files:
        src, _nl = read_src(py)
        bad = check(src)
        if bad:
            tally[py] = bad
            print(f"  {','.join(bad):14s} {rel(py)}")
    if not tally:
        print("  위반 없음")
    errs = sum(1 for v in tally.values() if any(x.startswith("E") for x in v))
    print(f"\n검사 {len(files)}개 / 위반 {len(tally)}개 (고쳐야 할 것 {errs}개)")
    return tally


def cmd_test(files):
    ok = bad = 0
    for py in files:
        d = os.path.dirname(py)
        if not testcases(d):
            continue
        allok = True
        for ip, op in testcases(d):
            good, got, why = run(py, ip)
            want = io.open(op, encoding="utf-8", errors="replace").read().split()
            if not good or got != want:
                allok = False
                print(f"  ✗ {rel(py)}  {why or ('want=' + str(want[:3]) + ' got=' + str(got[:3]))}")
                break
        ok, bad = (ok + 1, bad) if allok else (ok, bad + 1)
    print(f"\n저장된 정답과 일치 {ok} / 불일치 {bad}")
    print("※ 불일치가 곧 오답은 아니다 — 저장본이 예제 출력일 수 있다(부동소수 등).")


def cmd_fix(files):
    changed, reverted, skipped = [], [], []
    for py in files:
        src, nl = read_src(py)
        if not any(x.startswith("E") for x in check(src)):
            continue
        new = fix(src)
        if new == src:
            continue
        if not testcases(os.path.dirname(py)):
            skipped.append(py)                  # 테스트가 없으면 증명할 수 없다 → 안 고친다
            continue
        before = outputs_of(py)                 # ① 고치기 전 출력
        write_src(py, new, nl)
        after = outputs_of(py)                  # ② 고친 뒤 출력
        if before == after:
            changed.append(py)
        else:
            write_src(py, src, nl)              # ③ 다르면 되돌린다
            reverted.append((py, before, after))

    for p in changed:
        print(f"  고침   {rel(p)}")
    for p, b, a in reverted:
        print(f"  되돌림 {rel(p)}  ← 출력이 바뀐다")
        for (n1, o1, g1, w1), (n2, o2, g2, w2) in zip(b, a):
            if (o1, g1, w1) != (o2, g2, w2):
                print(f"           {n1}: 전 {g1[:3] or w1} / 후 {g2[:3] or w2}")
    for p in skipped:
        print(f"  건너뜀 {rel(p)}  ← 테스트가 없어 증명 불가")
    print(f"\n고친 파일 {len(changed)} / 되돌린 파일 {len(reverted)} / 건너뛴 파일 {len(skipped)}")
    if reverted:
        print("되돌린 것은 손으로 보셔야 합니다 — 규칙이 못 잡는 무언가가 있습니다.")


def main():
    args = sys.argv[1:]
    files = solution_files()
    print(f"대상: {rel(SOLUTION_ROOT)}/**/*.py  ({len(files)}개)   ※ study/ref/ 는 제외\n")
    if "--fix" in args:
        cmd_fix(files)
    elif "--test" in args:
        cmd_test(files)
    else:
        cmd_check(files)


if __name__ == "__main__":
    main()
