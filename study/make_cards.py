# -*- coding: utf-8 -*-
"""Qwen 에게 카드를 만들게 하고, 검사기로 판정해서 통과한 것만 남긴다.

    python study/make_cards.py --n 3          완전검증 가능한 것부터 3장
    python study/make_cards.py 2231 2798      번호 지정
    python study/make_cards.py --n 3 --dry    프롬프트만 보고 호출은 안 함

★ TOTL(100.96.0.6) 에서 돌린다 — Qwen 이 127.0.0.1:8081 에 떠 있다.

설계 원칙 (260921-하네스스킬.md): **판정을 LLM 에게 맡기지 않는다.**
  만드는 것만 Qwen 이 하고, 통과/거부는 build.py(형식) + verify_cards.py(사실)가 정한다.
  거부되면 사유를 프롬프트에 붙여 다시 시킨다. 3번 실패하면 파일을 지우고 넘어간다
  (반쯤 맞는 카드를 남기면 그게 그대로 출제된다).

머리말은 Qwen 에게 맡기지 않고 **우리가 직접 쓴다.** 번호·제목·난이도·분류는 이미 알고 있고,
Qwen 이 여기서 틀리면(tier·cat 오타) C6 로 거부돼 재시도를 낭비한다. Qwen 은 본문만 쓴다.
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import glob
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CARDS = os.path.join(HERE, "cards")
REF = os.path.join(HERE, "ref")
PROMPT_MD = os.path.join(CARDS, "PROMPT.md")
LLM = "http://127.0.0.1:8081/v1/chat/completions"

sys.path.insert(0, HERE)
import verify_cards as vc                                  # noqa: E402

NEED_SEC = ["문제", "입력", "출력", "예제", "풀이 아이디어", "코드 따라가기", "외울 것"]


def llm(prompt, max_tokens=4000, temp=0.3, timeout=600):
    """Qwen 한 번 호출. thinking 은 끈다 — 켜두면 content 가 비고 토큰만 태운다."""
    body = json.dumps({
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temp,
        "chat_template_kwargs": {"enable_thinking": False},
    }).encode("utf-8")
    req = urllib.request.Request(LLM, data=body,
                                headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.load(r)
    return (d["choices"][0]["message"].get("content") or "").strip()


def todo():
    """build.py --todo 를 그대로 믿는다 (문제 목록의 정본은 그쪽이다)."""
    out = subprocess.run([sys.executable, os.path.join(CARDS, "build.py"), "--todo"],
                         capture_output=True, text=True, encoding="utf-8").stdout
    rows = re.findall(r"^\s{2}(\S+)\s+(\d+)\s+(.+?)\s{2,}(\S.*)$", out, re.M)
    return [(c, n, t.strip(), ti.strip()) for c, n, t, ti in rows]


def verifiable(rows):
    """README + 테스트가 있어 C1·C2·C3 까지 볼 수 있는 것만. 검증 못 할 카드는 안 만든다."""
    out = []
    for cat, no, title, tier in rows:
        ds = [d for d in glob.glob(os.path.join(REPO, "Python", "*", "*", no + "*"))
              if os.path.isdir(d)]
        if ds and os.path.exists(os.path.join(ds[0], "README.md")) \
                and glob.glob(os.path.join(ds[0], "input*.txt")):
            out.append((cat, no, title, tier))
    return out


def prompt_template():
    """PROMPT.md 의 ===== 사이를 그대로 쓴다. 규칙이 한 곳에만 있게 한다."""
    t = io.open(PROMPT_MD, encoding="utf-8", errors="replace").read()
    # ⚠ 그냥 split("=====") 하면 안 된다 — 안내문에 인라인 `=====` 가 있어서
    #   거기서 쪼개진다. **줄 전체가 ===== 인 곳**만 구획으로 본다.
    parts = re.split(r"(?m)^=====[ \t]*$", t)
    if len(parts) < 3:
        raise SystemExit("PROMPT.md 에서 ===== 구획(줄 전체)을 못 찾았다")
    return parts[1].strip()


def build_prompt(cat, no, title, tier, code, readme, retry_reasons=()):
    p = prompt_template()
    for k, v in (("{번호}", no), ("{제목}", title), ("{난이도}", tier),
                 ("{분류}", cat), ("{코드}", code)):
        p = p.replace(k, v)
    # 지문을 같이 준다 — 코드만 주면 입력 형식·제약을 코드에서 짐작하다 지어낸다.
    p += ("\n\n## 문제 지문 원문 (여기 있는 내용만 쓴다)\n"
          "<지문>\n" + vc.strip_markup(readme)[:6000] + "\n</지문>\n")
    p += ("\n## 출력 형식 — 이것만 지켜라\n"
          "`---` 머리말은 내가 붙인다(번호·제목·난이도·분류는 이미 안다). 너는 이렇게 쓴다:\n"
          "1) **첫 줄**에 `topic: ` 한 줄. 세부 유형을 짧게. 예: `완전탐색 · 3중 반복문`,\n"
          "   `DP · 1차원 점화식`, `문자열 · 해시`. 난이도나 분류 이름을 그대로 쓰지 마라.\n"
          "2) 빈 줄 하나\n"
          "3) `## 문제` 부터 일곱 개 항목\n"
          "\n`## 입력` 에는 지문에 적힌 **크기 제약(N, M 의 범위)을 그대로** 옮겨라. "
          "지문에 없으면 쓰지 마라 — 숫자를 짐작하지 마라.\n")
    if retry_reasons:
        p += ("\n## ⚠ 직전 시도가 거부됐다. 아래를 고쳐서 다시 써라\n"
              + "\n".join("- " + r for r in retry_reasons) + "\n")
    return p


def clean_body(text):
    """Qwen 출력 다듬기 -> (topic, 본문).

    ⚠ topic 을 먼저 떼고 나서 `## 문제` 앞을 자른다. 순서를 바꾸면 topic 줄이 먼저
      잘려나가서 항상 기본값이 들어간다(첫판에 그랬다).
    """
    t = text.strip()
    if t.startswith("```"):                       # 전체를 코드펜스로 감싼 경우
        t = re.sub(r"^```[a-z]*\n", "", t)
        t = re.sub(r"\n```$", "", t)
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S).strip()   # 머리말을 썼으면 버린다
    topic = ""
    m = re.match(r"topic:\s*(.+)", t)
    if m:
        topic = m.group(1).strip().strip("`")
        t = t[m.end():].lstrip("\n")
    i = t.find("## 문제")
    return topic, (t[i:].strip() if i >= 0 else t.strip())


def write_card(cat, no, title, tier, body, topic):
    d = os.path.join(CARDS, cat)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, no + ".md")
    head = (f"---\nno: {no}\ntitle: {title}\ntier: {tier}\ncat: {cat}\n"
            f"topic: {topic}\n---\n\n")
    io.open(p, "w", encoding="utf-8", newline="\n").write(head + body + "\n")
    return p


def judge(no):
    """형식(build.py) + 사실(verify_cards) 판정 -> 거부 사유 목록."""
    reasons = []
    r = subprocess.run([sys.executable, os.path.join(CARDS, "build.py")],
                       capture_output=True, text=True, encoding="utf-8")
    for line in (r.stdout or "").splitlines():
        if "[X]" in line and no in line:
            reasons.append("형식: " + line.strip())
    errs, _warns = vc.verify(no)
    reasons += errs
    return reasons


def make(cat, no, title, tier, tries=3, dry=False):
    ref = os.path.join(REF, no + ".py")
    if not os.path.exists(ref):
        return False, [f"ref/{no}.py 가 없다"]
    code = io.open(ref, encoding="utf-8", errors="replace").read()
    ds = [d for d in glob.glob(os.path.join(REPO, "Python", "*", "*", no + "*"))
          if os.path.isdir(d)]
    readme = ""
    if ds and os.path.exists(os.path.join(ds[0], "README.md")):
        readme = io.open(os.path.join(ds[0], "README.md"),
                         encoding="utf-8", errors="replace").read()

    reasons = []
    for attempt in range(1, tries + 1):
        p = build_prompt(cat, no, title, tier, code, readme, reasons)
        if dry:
            print(p[:1500] + "\n...(생략)")
            return True, []
        t0 = time.time()
        try:
            topic, body = clean_body(llm(p))
        except Exception as e:
            return False, [f"Qwen 호출 실패: {type(e).__name__}: {e}"]
        if not topic:
            topic = f"{tier} · {cat}"            # Qwen 이 안 썼을 때만 기본값
        missing = [s for s in NEED_SEC if ("## " + s) not in body]
        write_card(cat, no, title, tier, body, topic)
        reasons = ([f"항목 누락: {', '.join(missing)}"] if missing else []) + judge(no)
        print(f"      시도 {attempt}: {time.time()-t0:5.1f}s "
              f"{'통과' if not reasons else '거부 ' + str(len(reasons)) + '건'}")
        for r in reasons[:4]:
            print(f"         - {r[:88]}")
        if not reasons:
            return True, []
    # 3번 실패 -> 남기지 않는다. 반쯤 맞는 카드는 그대로 출제되어 해롭다.
    p = os.path.join(CARDS, cat, no + ".md")
    if os.path.exists(p):
        os.remove(p)
    return False, reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nos", nargs="*")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--tries", type=int, default=3)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    rows = todo()
    pick = verifiable(rows)
    if a.nos:
        pick = [r for r in rows if r[1] in a.nos]
    else:
        pick = pick[:a.n]
    if not pick:
        print("만들 카드가 없다 (완전검증 가능한 것이 남지 않았다)")
        return 0

    print(f"만들 카드 {len(pick)}장 — 검증 못 할 카드는 애초에 만들지 않는다\n")
    ok, bad = [], []
    for cat, no, title, tier in pick:
        print(f"  {no} {title} ({tier}, {cat})")
        good, reasons = make(cat, no, title, tier, a.tries, a.dry)
        (ok if good else bad).append(no)
        if not good:
            print(f"      → 포기. 카드 파일을 지웠다")
    print(f"\n통과 {len(ok)} / 포기 {len(bad)}")
    if ok:
        print("통과:", " ".join(ok))
    if bad:
        print("포기:", " ".join(bad), " ← 손으로 만들거나 프롬프트를 고쳐야 한다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
