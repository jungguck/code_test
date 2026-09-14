"""BOJ-style judge.

usage:
    python training/boj/judge.py p01_sort_desc
    python training/boj/judge.py            (all problems)
"""
import io
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))


def judge(prob):
    d = os.path.join(BASE, prob)
    sol = os.path.join(d, "solution.py")
    tdir = os.path.join(d, "tests")
    ins = sorted(f for f in os.listdir(tdir) if f.endswith(".in"))
    ok_all = True
    print(f"=== {prob} ===")
    for fin in ins:
        num = fin[:-3]
        with io.open(os.path.join(tdir, fin), encoding="utf-8") as f:
            data = f.read()
        with io.open(os.path.join(tdir, num + ".out"), encoding="utf-8") as f:
            want = f.read()
        p = subprocess.run(
            [sys.executable, sol], input=data, capture_output=True,
            text=True, encoding="utf-8",
        )
        got = p.stdout
        norm = lambda s: "\n".join(l.rstrip() for l in s.strip().splitlines())
        if p.returncode != 0:
            ok_all = False
            print(f"  [RTE ] test {num}")
            print("    " + (p.stderr.strip().splitlines() or ["?"])[-1])
        elif norm(got) == norm(want):
            print(f"  [PASS] test {num}")
        else:
            ok_all = False
            print(f"  [FAIL] test {num}")
            print(f"    input : {norm(data)!r}")
            print(f"    got   : {norm(got)!r}")
            print(f"    want  : {norm(want)!r}")
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
