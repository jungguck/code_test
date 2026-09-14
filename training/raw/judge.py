"""RAW mode judge -- correctness + banned-builtin check + time limit.

usage:
    python training/raw/judge.py r01_sort
    python training/raw/judge.py
"""
import io
import os
import re
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
TIME_LIMIT = 5.0


def strip_comments(src):
    """주석/문자열 안의 금지어는 봐준다 (설명 적으라고)."""
    src = re.sub(r'"""[\s\S]*?"""', '', src)
    src = re.sub(r"'''[\s\S]*?'''", '', src)
    src = re.sub(r'#.*', '', src)
    src = re.sub(r'"[^"\n]*"', '""', src)
    src = re.sub(r"'[^'\n]*'", "''", src)
    return src


def read_list(path):
    if not os.path.exists(path):
        return []
    with io.open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def check_banned(d, sol):
    banned = read_list(os.path.join(d, "banned.txt"))
    if not banned:
        return True
    with io.open(sol, encoding="utf-8") as f:
        code = strip_comments(f.read())
    # allowed.txt 에 적힌 표현은 검사 전에 지워서 예외 처리한다
    # (예: 직접 만든 Stack 의 stack.pop() 은 허용, 리스트의 lst.pop() 은 금지)
    for a in read_list(os.path.join(d, "allowed.txt")):
        code = code.replace(a, "")
    hits = [b for b in banned if b in code]
    if hits:
        print("  [BAN ] 금지된 기능 사용: " + ", ".join(repr(h) for h in hits))
        print("         -> 직접 구현해야 함")
        return False
    return True


def judge(prob):
    d = os.path.join(BASE, prob)
    sol = os.path.join(d, "solution.py")
    tdir = os.path.join(d, "tests")
    print(f"=== {prob} ===")
    if not check_banned(d, sol):
        return False
    ok_all = True
    for fin in sorted(f for f in os.listdir(tdir) if f.endswith(".in")):
        num = fin[:-3]
        with io.open(os.path.join(tdir, fin), encoding="utf-8") as f:
            data = f.read()
        with io.open(os.path.join(tdir, num + ".out"), encoding="utf-8") as f:
            want = f.read()
        t0 = time.perf_counter()
        try:
            p = subprocess.run(
                [sys.executable, sol], input=data, capture_output=True,
                text=True, encoding="utf-8", timeout=TIME_LIMIT,
            )
        except subprocess.TimeoutExpired:
            ok_all = False
            print(f"  [TLE ] test {num}  (>{TIME_LIMIT}s) -- 알고리즘이 너무 느림")
            continue
        el = time.perf_counter() - t0
        norm = lambda s: "\n".join(l.rstrip() for l in s.strip().splitlines())
        if p.returncode != 0:
            ok_all = False
            print(f"  [RTE ] test {num}")
            print("    " + (p.stderr.strip().splitlines() or ["?"])[-1])
        elif norm(p.stdout) == norm(want):
            print(f"  [PASS] test {num}   ({el:.2f}s)")
        else:
            ok_all = False
            g, w = norm(p.stdout), norm(want)
            cut = lambda s: s if len(s) <= 90 else s[:90] + " ...(생략)"
            print(f"  [FAIL] test {num}")
            print(f"    got : {cut(g)!r}")
            print(f"    want: {cut(w)!r}")
    return ok_all


targets = sys.argv[1:] or sorted(
    x for x in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, x))
)
results = [(t, judge(t)) for t in targets]
print("-" * 50)
if all(ok for _, ok in results):
    print("ALL PASS  <<< done!")
    sys.exit(0)
for t, ok in results:
    print(f"{'OK  ' if ok else 'FAIL'}  {t}")
sys.exit(1)
