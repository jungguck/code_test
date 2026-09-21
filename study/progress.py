# -*- coding: utf-8 -*-
"""진행률 갱신기.

백준에서 문제를 풀면 BaekjoonHub 확장이 이 레포의
`Python/백준/<티어>/<번호>. <제목>/` 으로 자동 커밋한다.
이 스크립트는 그 폴더명에서 문제 번호를 읽어서
체크리스트의 체크박스를 자동으로 갱신한다.

    python study/progress.py
"""
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # 레포 루트

TIERS = ["Unrated"] + [
    f"{name} {num}"
    for name in ("Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby")
    for num in ("V", "IV", "III", "II", "I")
]


def solved_numbers():
    """BaekjoonHub 가 올려둔 폴더들을 훑어서 푼 문제 번호를 모은다."""
    found = set()
    for base, dirs, _ in os.walk(ROOT):
        if os.sep + ".git" in base:
            continue
        for d in dirs:
            m = re.match(r"^(\d+)\.\s", d)
            if m:
                found.add(m.group(1))
    return found


def table(problems, solved):
    lines = [
        "| ✓ | 번호 | 문제 | 난이도 | 참고 |",
        "|:-:|:-:|---|:-:|:-:|",
    ]
    for p in problems:
        no = p["no"]
        check = "✅" if no in solved else "⬜"
        tier = TIERS[p["tier"]] if 0 <= p["tier"] < len(TIERS) else "Unrated"
        ref = f"[py](../ref/{no}.py)" if p["ref"] else "—"
        lines.append(
            f"| {check} | [{no}](https://www.acmicpc.net/problem/{no}) "
            f"| {p['title']} | {tier} | {ref} |"
        )
    return "\n".join(lines)


def bar(done, total, width=24):
    filled = 0 if total == 0 else round(width * done / total)
    return "█" * filled + "░" * (width - filled)


def main():
    data = json.load(open(os.path.join(HERE, "problems.json"), encoding="utf-8"))
    solved = solved_numbers()

    summary, grand_done, grand_total = [], 0, 0
    for group, info in sorted(data.items()):
        problems = info["problems"]
        done = sum(1 for p in problems if p["no"] in solved)
        grand_done += done
        grand_total += len(problems)

        body = (
            f"# {info['title']}\n\n"
            f"[⬅ 전체 목록](../README.md)\n\n"
            f"**{done} / {len(problems)}**  `{bar(done, len(problems))}`\n\n"
            f"난이도 오름차순. `참고` 는 남의 파이썬 풀이 — **먼저 스스로 풀고** 열 것.\n\n"
            f"{table(problems, solved)}\n"
        )
        d = os.path.join(HERE, group)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "README.md"), "w", encoding="utf-8") as f:
            f.write(body)

        summary.append(
            f"| [{info['title']}]({group}/README.md) "
            f"| {done} / {len(problems)} | `{bar(done, len(problems), 16)}` |"
        )
        print(f"{group:22s} {done:3d} / {len(problems):3d}")

    index = (
        "# 백준 코딩테스트 훈련 📘\n\n"
        f"**{grand_done} / {grand_total}**  `{bar(grand_done, grand_total)}`\n\n"
        "| 분류 | 진행 | |\n|---|:-:|---|\n"
        + "\n".join(summary)
        + "\n\n## 하는 법\n\n"
        "1. 위 분류에서 하나 골라 들어간다 (난이도순으로 정렬돼 있음)\n"
        "2. 맨 위 안 푼 문제(⬜)의 번호를 눌러 백준으로 간다\n"
        "3. 백준에서 풀고 제출한다 → BaekjoonHub 확장이 자동으로 커밋해준다\n"
        "4. 체크 갱신:\n\n"
        "   ```\n   git pull\n   python study/progress.py\n   git add -A && git commit -m \"progress\" && git push\n   ```\n\n"
        "막히면 `참고` 링크의 풀이를 본다. **단, 30분은 혼자 붙잡아본 뒤에.**\n\n"
        "## 예전 훈련장\n\n"
        "`training/` 에 손으로 만든 연습문제가 남아있다 "
        "(quiz 14문제 · RAW 모드 · 문법 노트).\n"
        "문법이 헷갈리면 `training/quiz/SYNTAX.md` 를 볼 것.\n\n"
        "## 출처\n\n"
        "문제 선정과 분류는 [tony9402/baekjoon](https://github.com/tony9402/baekjoon) 문제집,\n"
        "참고 풀이는 [tony9402/algorithm-solutions](https://github.com/tony9402/algorithm-solutions) 에서 가져왔다.\n"
    )
    with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
        f.write(index)

    print(f"{'합계':22s} {grand_done:3d} / {grand_total:3d}")


if __name__ == "__main__":
    main()
