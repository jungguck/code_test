# -*- coding: utf-8 -*-
"""카드가 **사실과 맞는지** 검사한다. build.py 가 형식을 보고, 이 파일이 내용을 본다.

    python study/verify_cards.py              전체 검사
    python study/verify_cards.py 15829 32941   특정 카드만

왜 필요한가 — 카드는 Qwen 이 쓴다. LLM 은 지문에 없는 숫자를 만들어내고, 없는 코드를
인용하고, 예제 답을 상상한다. 실제로 그렇게 틀렸다(2026-09-28):

    15829  README 에 없는 'L ≤ 100,000' 을 지어냄
    32941  입력 형식 전체를 틀림 (첫 줄 'T X' 인데 'T, N, X' / 조원정보 2N줄인데 N줄)

그래서 **판정은 사람이나 LLM 이 아니라 코드가 한다** (260921-하네스스킬.md 원칙).
사람은 거부된 것만 본다 — 카드가 늘어나도 검수 비용이 늘지 않는다.

검사 항목
    C1 숫자 근거    카드가 말하는 수치 제약이 README 에 실제로 있는가      ★ 지어내기 차단
    C2 예제 근거    저장된 정답(output*)이 카드 예제 코드블록에 있는가       ★ 상상 차단
    C3 정답 코드    ref/{번호}.py 가 저장된 테스트를 통과하는가
    C4 코드 인용    카드의 python 블록이 정답 코드에 실제로 있는가         (경고만)
    C5 금지어       C++ 내용이 섞였는가                                   ★ 파이썬 전용
    C6 일관성       머리말 no 와 파일명, 제목이 problems.json 과 맞는가

C4 만 경고다 — 설명용 미니 예시는 정답 코드에 없는 게 정상이기 때문이다. 나머지는 거부.
"""
import io
import json
import os
import re
import subprocess
import sys
import glob

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CARDS = os.path.join(HERE, "cards")
REF = os.path.join(HERE, "ref")
SOLUTION_ROOT = os.path.join(REPO, "Python")

# ── 지문 태그 걷어내기 (bot.py 의 strip_boj_markup 과 같은 규칙) ──────────
_MJX_TAG = re.compile(r"</?mjx-[^>]*>")
_TEX_DUP = re.compile(r"\$[^$\n]{0,300}\$")
_ANY_TAG = re.compile(r"<[^>]+>")


def strip_markup(text):
    if not text or ("mjx-" not in text and "<p>" not in text):
        return text or ""
    t = _MJX_TAG.sub("", text)
    t = _TEX_DUP.sub("", t)
    t = _ANY_TAG.sub("", t)
    for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return t


def digits(text):
    """숫자 집합.

    ⚠ 콤마를 통째로 지우면 안 된다 — `[1,3,4]` 가 `134` 로 뭉쳐져 없는 숫자가 생긴다
      (2026-09-28 첫판에서 32941 카드가 이것 때문에 거부됐다).
      천 단위 구분(1,000)만 붙여 읽고, 나머지 콤마는 구분자로 둔다.
    """
    t = (text or "").replace(" ", " ")            # 제목에 섞인 특수 공백
    t = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", t)      # 1,000 -> 1000 (구분자만)
    return set(re.findall(r"\d+", t))


def parse_card(path):
    """카드 -> (머리말, {항목: 본문}). build.py 와 같은 방식으로 쪼갠다."""
    lines = io.open(path, encoding="utf-8", errors="replace").read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None
    meta, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            meta[k.strip()] = v.strip()
        i += 1
    sec, cur, buf = {}, None, []
    for line in lines[i + 1:]:
        if line.startswith("## "):
            if cur is not None:
                sec[cur] = "\n".join(buf).strip()
            cur = line[3:].strip().lstrip("⚠️ ").strip()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        sec[cur] = "\n".join(buf).strip()
    return meta, sec


def problem_dir(no):
    """그 번호의 문제 폴더 (README·input·output 이 있는 곳)."""
    for d in glob.glob(os.path.join(SOLUTION_ROOT, "*", "*", no + ".*")):
        if os.path.isdir(d):
            return d
    for d in glob.glob(os.path.join(SOLUTION_ROOT, "*", "*", no + " *")):
        if os.path.isdir(d):
            return d
    return None


def testcases(d):
    pairs = []
    for ip in sorted(glob.glob(os.path.join(d, "input*.txt"))):
        n = re.sub(r"\D", "", os.path.basename(ip))
        op = os.path.join(d, "output" + n + ".txt")
        if os.path.exists(op):
            pairs.append((ip, op))
    return pairs


def code_blocks(text):
    """```python ... ``` 블록들."""
    return re.findall(r"```(?:python|py)?\n(.*?)```", text or "", re.S)


def norm_code(s):
    """비교용 정규화 — 공백과 **주석**을 없앤다.

    ⚠ 주석을 지워야 한다. 카드는 인용한 코드에 설명 주석을 달아서 가르친다
      (`empty, virus = get_pos()   # 빈 칸 목록`). 주석을 코드로 세면 "정답 코드에 없음"
      으로 오탐한다(2026-09-28 첫판에서 14502 카드가 이것 때문에 거부됐다).
    """
    t = re.sub(r"#[^\n]*", "", s or "")        # 줄 끝 주석 제거
    return re.sub(r"\s+", "", t)


def verify(no):
    """카드 1장 -> (거부 사유 목록, 경고 목록)."""
    errs, warns = [], []
    hits = glob.glob(os.path.join(CARDS, "*", no + ".md"))
    if not hits:
        return ["카드 파일이 없다"], []
    card = hits[0]
    meta, sec = parse_card(card)
    if meta is None:
        return ["머리말(---)이 없다"], []

    ref = os.path.join(REF, no + ".py")
    if not os.path.exists(ref):
        errs.append(f"ref/{no}.py 가 없다")
    d = problem_dir(no)
    readme = ""
    if d and os.path.exists(os.path.join(d, "README.md")):
        readme = strip_markup(io.open(os.path.join(d, "README.md"),
                                     encoding="utf-8", errors="replace").read())
    else:
        warns.append("문제 폴더/README 를 못 찾아 C1 을 건너뛴다")

    body = "\n".join(sec.values()) if sec else ""

    # ── C6 일관성 ───────────────────────────────────────────────
    if meta.get("no") != no:
        errs.append(f"머리말 no={meta.get('no')} 가 파일명({no})과 다르다")
    if meta.get("cat") and os.path.basename(os.path.dirname(card)) != meta["cat"]:
        errs.append(f"머리말 cat={meta['cat']} 가 폴더({os.path.basename(os.path.dirname(card))})와 다르다")

    # ── C5 금지어 ───────────────────────────────────────────────
    #   ⚠ 언어 이름 언급은 막지 않는다. "C++ 이라면 오버플로로 깨진다" 같은 **대조**는
    #     좋은 설명이다(2026-09-28 첫판에서 15829 카드가 이것 때문에 거부됐다).
    #     실제 C++ **코드**가 들어온 것만 거부한다.
    for bad in ("#include", "std::", "cout <<", "cin >>", "using namespace"):
        if bad in body:
            errs.append(f"C++ 코드가 섞였다: {bad!r}")
            break

    # ── C1 숫자 근거 ─ 카드의 '입력' 절 수치가 README 에 실제로 있는가
    if readme and sec and sec.get("입력"):
        rd = digits(readme)
        # 2자리 이상만 본다. 한 자리는 '두 줄', '1번째' 같은 서술과 섞여 오탐이 많다.
        for n2 in sorted(x for x in digits(sec["입력"]) if len(x) >= 2):
            if n2 not in rd:
                errs.append(f"C1 '입력' 절의 숫자 {n2} 가 README 에 없다 (지어낸 값 의심)")

    # ── C2 예제 근거 ─ **저장된 정답이 카드 예제에 나오는가** (방향이 중요하다)
    #   첫판에는 거꾸로 봤다 — "카드의 숫자가 input/output 에 있는가". 그러면 유도식
    #   (1×1 + 2×31 + 3×961 …)의 중간값이 전부 거부됐다. 잡아야 하는 것은 그게 아니라
    #   **카드가 엉뚱한 답을 적는 것**이다. 그래서 정답 -> 카드 방향으로 본다.
    #   (카드에 숫자가 더 많은 건 설명이니 정상이다)
    if d and sec and sec.get("예제"):
        # ⚠ 절 전체가 아니라 **코드블록(실제 예제 I/O)** 을 본다.
        #   첫판에는 절 전체를 봤더니, 해설 산문에 정답 숫자가 우연히 있으면 통과했다
        #   (자체시험에서 '4739715 -> 9999999' 주입을 놓쳤다).
        fenced = "\n".join(re.findall(r"```[a-z]*\n(.*?)```", sec["예제"], re.S))
        scope = fenced if fenced.strip() else sec["예제"]
        ex = digits(scope)
        # 규칙: **카드가 그 테스트의 입력을 보여준다면, 그 답도 맞게 적혀 있어야 한다.**
        #   "저장된 모든 테스트의 답이 있어야 한다" 로 하면 안 된다 — 카드가 예제를 하나만
        #   보여주는 것은 정상인데 거부된다(32941 이 그래서 거부됐다).
        #   입력이 카드에 있는 테스트만 골라서 그 답을 대조한다.
        shown = 0
        for ip, op in testcases(d):
            itxt = io.open(ip, encoding="utf-8", errors="replace").read()
            idig = digits(itxt)
            if idig and not idig <= ex:
                continue                       # 이 테스트는 카드에 안 실렸다 → 볼 것 없다
            shown += 1
            otxt = io.open(op, encoding="utf-8", errors="replace").read()
            odig = digits(otxt)
            missing = sorted(x for x in odig if x not in ex)
            if missing:
                # 출력이 긴 문제(알파벳 찾기: 26개 토큰)는 카드가 예제를 줄여 쓰는 것이
                #   정상이다. 그때까지 거부하면 만들 수 없는 카드가 된다 → 경고로 낮춘다.
                #   짧은 출력에서 답이 틀린 것은 그대로 거부한다(그게 잡아야 할 것이다).
                if len(otxt.split()) > 8:
                    warns.append(f"C2 {os.path.basename(ip)} 의 정답 일부({missing[:4]})가 "
                                 f"예제에 없다 — 출력이 길어 줄여 쓴 것이면 정상")
                else:
                    errs.append(f"C2 {os.path.basename(ip)} 는 예제에 실렸는데 그 정답 "
                                f"{missing} 가 없다")
            for tok in otxt.split():           # YES/NO 처럼 숫자가 아닌 정답
                if tok and not tok.isdigit() and tok not in scope:
                    errs.append(f"C2 {os.path.basename(ip)} 는 예제에 실렸는데 그 정답 "
                                f"{tok!r} 가 없다")
        if not shown:
            warns.append("C2 저장된 테스트 중 카드 예제에 실린 것이 없어 대조를 못 했다")

    # ── C3 정답 코드가 실제로 통과하는가
    if d and os.path.exists(ref):
        for ip, op in testcases(d):
            want = io.open(op, encoding="utf-8", errors="replace").read().split()
            try:
                with io.open(ip, "rb") as f:
                    r = subprocess.run([sys.executable, ref], stdin=f,
                                       capture_output=True, timeout=10)
            except subprocess.TimeoutExpired:
                errs.append(f"C3 ref/{no}.py TIMEOUT ({os.path.basename(ip)})")
                break
            got = r.stdout.decode("utf-8", "replace").split()
            if r.returncode != 0:
                errs.append(f"C3 ref/{no}.py 실행 실패 ({os.path.basename(ip)})")
                break
            if got != want:
                warns.append(f"C3 ref/{no}.py 출력이 저장본과 다르다 "
                             f"(기대 {want[:2]} / 실제 {got[:2]}) — 부동소수나 저장본 오류일 수 있다")
                break

    # ── C7 생각 흘림 / 추측 표현 ────────────────────────────────
    #   Qwen 이 답을 못 찾으면 **고민을 본문에 남긴다.** 실측(2775 부녀회장):
    #     "아니, 규칙을 다시 보면 …", "Wait, 예제 출력이 …", "예제 형식이 혼재되어 있거나"
    #   숫자는 다 들어있어서 C2 를 통과했다 — 그래서 별도 규칙이 필요하다.
    #   근거: .claude/commands/explain.md "겸손 표현 말고 **단정적으로**".
    for mark in ("Wait", "Hmm", "Let me", "Actually,", "아니,", "것 같다", "듯하다",
                 "아마도", "제 생각", "다시 보면", "혼재"):
        if mark in body:
            errs.append(f"C7 생각을 흘렸거나 추측 표현을 썼다: {mark!r} "
                        f"— 카드는 단정적으로 쓴다")
            break

    # ── C4 코드 인용 (경고) ─ 설명용 미니 예시는 없는 게 정상이다
    if os.path.exists(ref) and sec and sec.get("코드 따라가기"):
        refsrc = norm_code(io.open(ref, encoding="utf-8", errors="replace").read())
        blocks = code_blocks(sec["코드 따라가기"])
        quoted = sum(1 for b in blocks if norm_code(b) and norm_code(b) in refsrc)
        if blocks and quoted == 0:
            errs.append("C4 '코드 따라가기' 의 python 블록 중 정답 코드에 있는 것이 하나도 없다")
        elif len(blocks) - quoted:
            warns.append(f"C4 정답 코드에 없는 블록 {len(blocks)-quoted}개 "
                         f"(설명용 미니 예시면 정상)")

    return errs, warns


# ══════════════════════════════════════════════════════════════════════
# 자체시험 — 검사기가 정말 잡는지 증명한다
# ══════════════════════════════════════════════════════════════════════
# 다 통과하는 검사기는 쓸모가 없다. 과거에 **실제로 났던 오류**를 카드에 주입해서
# 거부되는지 본다. 카드는 finally 로 반드시 원본 복원한다.
#   첫판에 이 시험으로 결함 3개를 잡았다 — C2 가 절 전체를 봐서 산문에 정답 숫자가
#   우연히 있으면 통과했고, C5 가 언어 이름 언급만으로 거부했고, C4 가 주석 달린
#   인용을 '없는 코드' 로 봤다.

def _fence_swap(text, old, new):
    """'## 예제' 코드블록 안에서만 바꾼다 (실제 예제 I/O 를 건드리는 시험)."""
    m = re.search(r"(## 예제\n.*?```[a-z]*\n)(.*?)(```)", text, re.S)
    if not m or old not in m.group(2):
        return None
    return text[:m.start(2)] + m.group(2).replace(old, new) + text[m.end(2):]


_SELFTEST = [
    ("15829", "C1 없는 제약 지어내기",
     lambda t: t.replace("- 둘째 줄: 영문 소문자로만 이루어진 문자열",
                         "- 둘째 줄: 영문 소문자로만 이루어진 문자열 (1 ≤ L ≤ 100,000)", 1)),
    ("15829", "C2 예제 답 엉뚱하게", lambda t: _fence_swap(t, "4739715", "9999999")),
    ("15829", "C2 둘째 예제 답 틀리게", lambda t: _fence_swap(t, "25818", "25819")),
    ("32941", "C2 정답 NO -> YES", lambda t: _fence_swap(t, "NO", "YES")),
    ("32941", "C5 C++ 코드 삽입",
     lambda t: t.replace("## 외울 것", "## 외울 것\n```cpp\n#include <iostream>\n```\n", 1)),
    ("32941", "C6 머리말 no 불일치", lambda t: t.replace("no: 32941", "no: 32942", 1)),
    ("32941", "C7 생각 흘림",
     lambda t: t.replace("## 풀이 아이디어\n",
                         "## 풀이 아이디어\nWait, 규칙을 다시 보면 아닌 것 같다.\n", 1)),
]


def selftest():
    ok = miss = skip = 0
    print("자체시험 — 과거 실제 오류를 주입해 거부되는지 본다\n")
    print(f"{'시험':26s} {'결과':8s} 사유")
    print("-" * 88)
    for no, label, mut in _SELFTEST:
        hits = glob.glob(os.path.join(CARDS, "*", no + ".md"))
        if not hits:
            skip += 1
            print(f"{label:26s} {'스킵':8s} {no} 카드가 없다")
            continue
        p = hits[0]
        orig = io.open(p, encoding="utf-8", errors="replace").read()
        bad = mut(orig)
        if bad is None or bad == orig:
            skip += 1
            print(f"{label:26s} {'스킵':8s} 주입 지점 없음 (카드가 바뀐 듯)")
            continue
        try:
            io.open(p, "w", encoding="utf-8", newline="\n").write(bad)
            errs, _ = verify(no)
            if errs:
                ok += 1
            else:
                miss += 1
            print(f"{label:26s} {'잡음' if errs else '놓침!!':8s} "
                  f"{(errs[0][:58] if errs else '-')}")
        finally:
            io.open(p, "w", encoding="utf-8", newline="\n").write(orig)
    print(f"\n잡음 {ok} / 놓침 {miss} / 스킵 {skip}")
    if miss:
        print("놓친 것이 있다 — 검사기를 고쳐야 한다.")
    return 1 if miss else 0


def main():
    if "--selftest" in sys.argv[1:]:
        return selftest()
    want = [a for a in sys.argv[1:] if not a.startswith("-")]
    cards = sorted(glob.glob(os.path.join(CARDS, "*", "*.md")))
    cards = [c for c in cards if os.path.basename(c) != "PROMPT.md"]
    nos = [os.path.basename(c)[:-3] for c in cards]
    if want:
        nos = [n for n in nos if n in want]
    print(f"카드 {len(nos)}장 검사\n")
    okc = 0
    for no in nos:
        errs, warns = verify(no)
        if errs:
            print(f"  ✗ {no}")
            for e in errs:
                print(f"       거부  {e}")
        else:
            okc += 1
            print(f"  O {no}")
        for w in warns:
            print(f"       참고  {w}")
    print(f"\n통과 {okc} / 거부 {len(nos)-okc}")
    return 1 if okc != len(nos) else 0


if __name__ == "__main__":
    sys.exit(main())
