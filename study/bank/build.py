# -*- coding: utf-8 -*-
"""문제 폴더들을 모아 bank.json 하나로 만든다. (텔레그램 봇이 읽는 파일)

    python study/bank/build.py

각 문제 폴더 구성
    problem.md    문제 지문 (봇이 그대로 보낸다)
    solution.py   정답 코드
    explain.md    답지 해설 (틀렸을 때 보낸다)
    tests/N.in    입력
    tests/N.out   기대 출력
"""
import io
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))

CATEGORIES = [
    ("01_graph", "Graph 탐색 & 완전탐색", "BFS / DFS / 백트래킹"),
    ("02_ds",    "자료구조 응용",          "스택 / 큐 / 우선순위 큐 / 해시 / 투 포인터"),
    ("03_dp",    "동적 계획법",            "Dynamic Programming"),
]


def read(path):
    return io.open(path, encoding="utf-8").read().strip()


def run_tests(folder):
    """solution.py 가 tests/ 를 전부 통과하는지 확인. (실패 목록 반환)"""
    sol = os.path.join(folder, "solution.py")
    tdir = os.path.join(folder, "tests")
    fails = []
    for fin in sorted(f for f in os.listdir(tdir) if f.endswith(".in")):
        with io.open(os.path.join(tdir, fin), encoding="utf-8") as f:
            data = f.read()
        want = read(os.path.join(tdir, fin[:-3] + ".out"))
        p = subprocess.run([sys.executable, sol], input=data, capture_output=True,
                           text=True, encoding="utf-8", timeout=10)
        got = (p.stdout or "").strip()
        if got != want:
            fails.append((fin, want, got, (p.stderr or "").strip()[:200]))
    return fails


def main():
    bank, total, broken = [], 0, 0
    for key, title, subtitle in CATEGORIES:
        cdir = os.path.join(HERE, key)
        problems = []
        for name in sorted(os.listdir(cdir)):
            folder = os.path.join(cdir, name)
            if not os.path.isdir(folder):
                continue
            fails = run_tests(folder)
            if fails:
                broken += 1
                print("  [FAIL] %s/%s" % (key, name))
                for fin, want, got, err in fails:
                    print("     %s  want=%r got=%r %s" % (fin, want[:40], got[:40], err))
            tdir = os.path.join(folder, "tests")
            samples = []
            for fin in sorted(f for f in os.listdir(tdir) if f.endswith(".in")):
                samples.append({
                    "in":  read(os.path.join(tdir, fin)),
                    "out": read(os.path.join(tdir, fin[:-3] + ".out")),
                })
            problems.append({
                "id":       name,
                "category": key,
                "problem":  read(os.path.join(folder, "problem.md")),
                "solution": read(os.path.join(folder, "solution.py")),
                "explain":  read(os.path.join(folder, "explain.md")),
                "samples":  samples,
            })
            total += 1
        bank.append({"key": key, "title": title, "subtitle": subtitle,
                     "problems": problems})
        print("%-10s %2d문제" % (key, len(problems)))

    out = os.path.join(HERE, "bank.json")
    with io.open(out, "w", encoding="utf-8") as f:
        json.dump({"categories": bank}, f, ensure_ascii=False, indent=1)
    print("---")
    print("총 %d문제 -> bank.json" % total)
    if broken:
        print("!! 정답이 테스트를 통과 못한 문제 %d개 있음" % broken)
        return 1
    print("전부 정답 검증 통과")
    return 0


if __name__ == "__main__":
    sys.exit(main())
