# -*- coding: utf-8 -*-
"""카드(.md)를 검사하고 cards.json 하나로 묶는다. 텔레그램 봇은 이 json만 읽으면 된다.

    python study/cards/build.py           전체 검사 + 빌드
    python study/cards/build.py --todo    아직 안 만든 카드 목록만 출력

카드 한 장 = study/cards/<분류>/<문제번호>.md
정답 코드는 카드에 적지 않는다. study/ref/<문제번호>.py 에서 자동으로 가져온다.
"""
import io
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
REF = os.path.join(STUDY, "ref")

CATS = [
    ("01_graph", "Graph 탐색 & 완전탐색", "BFS / DFS / 백트래킹"),
    ("02_ds",    "자료구조 응용",          "스택 / 큐 / 우선순위 큐 / 해시 / 투 포인터"),
    ("03_dp",    "동적 계획법",            "Dynamic Programming"),
    ("04_etc",   "기타",                  "구현 / 수학 / 문자열 / 시뮬레이션"),
]

# 카드에 반드시 있어야 하는 항목 (순서 무관)
NEED_META = ["no", "title", "tier", "cat", "topic"]
NEED_SEC = ["문제", "입력", "출력", "예제", "풀이 아이디어", "코드 따라가기", "외울 것"]

# 봇이 "문제 메시지" 로 보낼 항목과 "답지 메시지" 로 보낼 항목
AS_PROBLEM = ["문제", "입력", "출력", "예제"]
AS_ANSWER = ["풀이 아이디어", "코드 따라가기", "외울 것", "이 코드의 버그"]


def parse(path):
    """카드 .md 를 {meta, sections} 로 쪼갠다. 문제가 있으면 (None, [사유]) 반환."""
    text = io.open(path, encoding="utf-8").read()
    lines = text.splitlines()
    problems = []

    # --- 머리말(frontmatter) 읽기 ---
    if not lines or lines[0].strip() != "---":
        return None, ["첫 줄이 --- 가 아님 (머리말 없음)"]
    meta, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            meta[k.strip()] = v.strip()
        i += 1
    if i >= len(lines):
        return None, ["머리말이 --- 로 닫히지 않음"]
    i += 1

    # --- '## 제목' 단위로 쪼개기 ---
    sections, cur, buf = {}, None, []
    for line in lines[i:]:
        if line.startswith("## "):
            if cur is not None:
                sections[cur] = "".join(x + chr(10) for x in buf).strip()
            cur = line[3:].strip().lstrip("⚠️ ").strip()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        sections[cur] = "".join(x + chr(10) for x in buf).strip()

    for k in NEED_META:
        if k not in meta:
            problems.append("머리말에 " + k + " 없음")
    for s in NEED_SEC:
        if s not in sections:
            problems.append("## " + s + " 항목 없음")
        elif len(sections[s]) < 10:
            problems.append("## " + s + " 내용이 너무 짧음")

    no = meta.get("no", "")
    base = os.path.basename(path)[:-3]
    if no and no != base:
        problems.append("머리말 no(" + no + ") 와 파일명(" + base + ") 불일치")
    if not os.path.exists(os.path.join(REF, base + ".py")):
        problems.append("ref/" + base + ".py 가 없음")

    return {"meta": meta, "sections": sections}, problems


def wanted():
    """만들어야 할 카드 전체 목록 (problems.json + ref 교집합)."""
    data = json.load(io.open(os.path.join(STUDY, "problems.json"), encoding="utf-8"))
    tiers = ["Unrated"]
    for name in ("Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"):
        for rank in ("V", "IV", "III", "II", "I"):
            tiers.append(name + " " + rank)
    key = {"01_graph_bruteforce": "01_graph", "02_data_structure": "02_ds", "03_dp": "03_dp", "04_etc": "04_etc"}
    out, seen = [], set()
    for g in sorted(data):
        for p in data[g]["problems"]:
            if p["no"] in seen or not os.path.exists(os.path.join(REF, p["no"] + ".py")):
                continue
            seen.add(p["no"])
            out.append({"cat": key[g], "no": p["no"], "title": p["title"],
                        "tier": tiers[p["tier"]] if p["tier"] < len(tiers) else "Unrated"})
    return out


def main():
    todo_only = "--todo" in sys.argv
    todo = []
    result, bad = [], 0

    for key, title, subtitle in CATS:
        cdir = os.path.join(HERE, key)
        if not os.path.isdir(cdir):
            os.makedirs(cdir)
        done = set()
        cards = []
        for name in sorted(os.listdir(cdir)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(cdir, name)
            card, errs = parse(path)
            if errs:
                bad += 1
                print("[X] " + key + "/" + name)
                for e in errs:
                    print("      " + e)
                continue
            no = name[:-3]
            done.add(no)
            code = io.open(os.path.join(REF, no + ".py"), encoding="utf-8").read().strip()
            sec = card["sections"]
            join = lambda keys: (chr(10) * 2).join(
                "## " + k + chr(10) + sec[k] for k in keys if k in sec)
            cards.append({
                "no": no,
                "title": card["meta"].get("title", ""),
                "tier": card["meta"].get("tier", ""),
                "topic": card["meta"].get("topic", ""),
                "category": key,
                "problem": join(AS_PROBLEM),
                "answer": join(AS_ANSWER),
                "code": code,
                "has_bug_note": "이 코드의 버그" in sec,
            })
        result.append({"key": key, "title": title, "subtitle": subtitle, "cards": cards})
        for w in wanted():
            if w["cat"] == key and w["no"] not in done:
                todo.append(w)
        print("%-10s 완성 %2d장" % (key, len(cards)))

    if todo_only:
        print()
        print("=== 아직 안 만든 카드 " + str(len(todo)) + "장 ===")
        for w in todo:
            print("  %-9s %-7s %-26s %s" % (w["cat"], w["no"], w["title"], w["tier"]))
        return 0

    total = sum(len(c["cards"]) for c in result)
    with io.open(os.path.join(HERE, "cards.json"), "w", encoding="utf-8") as f:
        json.dump({"categories": result}, f, ensure_ascii=False, indent=1)
    print("---")
    print("완성 " + str(total) + "장 / 남은 것 " + str(len(todo)) + "장  ->  cards.json")
    if bad:
        print("!! 형식이 깨진 카드 " + str(bad) + "장. 위 사유를 고칠 것")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
