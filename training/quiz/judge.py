"""QUIZ judge -- 표준입출력 채점 + 시간 측정.

usage:
    python training/quiz/judge.py q01_battery_log      # 한 문제
    python training/quiz/judge.py                      # 전체
"""
import io
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
TIME_LIMIT = 10.0


def norm(s):
    return "\n".join(l.rstrip() for l in s.strip().splitlines())


def judge(prob):
    d = os.path.join(BASE, prob)
    sol = os.path.join(d, "solution.py")
    tdir = os.path.join(d, "tests")
    print("=== %s ===" % prob)
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
            print("  [TLE ] test %s  (>%.0fs) -- 알고리즘이 너무 느림" % (num, TIME_LIMIT))
            continue
        el = time.perf_counter() - t0
        if p.returncode != 0:
            ok_all = False
            print("  [RTE ] test %s" % num)
            print("    " + (p.stderr.strip().splitlines() or ["?"])[-1])
        elif norm(p.stdout) == norm(want):
            print("  [PASS] test %s   (%.2fs)" % (num, el))
        else:
            ok_all = False
            cut = lambda s: s if len(s) <= 90 else s[:90] + " ...(생략)"
            print("  [FAIL] test %s" % num)
            print("    got : %r" % cut(norm(p.stdout)))
            print("    want: %r" % cut(norm(want)))
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
    print("%s  %s" % ("OK  " if ok else "FAIL", t))
sys.exit(1)
