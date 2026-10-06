#!/usr/bin/env python3
r"""校验各科模拟卷 tex 的卷面分值是否自洽。
规则:
  - 每份 mock-exam 必须出现 1 个 \examcover，第 4 个参数是满分
  - \qtypename{题型}{分值说明} 的第二个参数里所有 "N 分" 求和（去重后）
  - \parttitle{...（N 分）} 若含分则参与求和；若该 parttitle 下已用
    \qtypename 计过分，则不重复计入
  - 合计应等于 \examcover 的满分
用法: python3 exam-template/check_scores.py [目录过滤]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUM = r"(\d+(?:\.\d+)?)"


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        i, buf = 0, []
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            buf.append(line[i])
            i += 1
        out.append("".join(buf))
    return "\n".join(out)


def arg_groups(text: str, macro: str) -> list[list[str]]:
    r"""抓取 \macro{a}{b}... 的花括号参数（按平衡括号扫描，最多 8 个）。"""
    res = []
    for m in re.finditer(re.escape(macro) + r"\s*", text):
        i = m.end()
        args, ok = [], True
        while i < len(text) and text[i] == "{":
            depth, j = 0, i
            while j < len(text):
                if text[j] == "{" and (j == 0 or text[j - 1] != "\\"):
                    depth += 1
                elif text[j] == "}" and text[j - 1] != "\\":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if depth != 0:
                ok = False
                break
            args.append(text[i + 1:j])
            i = j + 1
            while i < len(text) and text[i] in " \t":
                i += 1
            if len(args) >= 8:
                break
        if ok and args:
            res.append(args)
    return res


def scores_in(s: str) -> float:
    """理解三种写法（可混用）：
      1) '...共 20 分'                -> 20
      2) '10 题，每题 2 分'           -> 20
      3) '4 题 × 5 分 = 20 分，共...' -> 20
    优先使用显式的 '共 N 分'，否则用题数×每题分。
    """
    m = re.search(r"共\s*" + NUM + r"\s*分", s)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+)\s*[题小]", s)
    n = int(m.group(1)) if m else None
    m2 = re.search(r"每\s*[题小]\s*" + NUM + r"\s*分", s)
    if n is not None and m2:
        return n * float(m2.group(1))
    # 兜底：所有 'N 分' 之和，但排除 'N 题'
    total = 0.0
    for mm in re.finditer(NUM + r"\s*分", s):
        total += float(mm.group(1))
    return total


def check(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    text = strip_comments(raw)
    msgs: list[str] = []
    covers = arg_groups(text, r"\examcover")
    if not covers:
        if arg_groups(text, r"\answercover"):
            return []          # 答案文件不校验分值
        msgs.append("缺少 \\examcover")
        return msgs
    full = covers[0][3] if len(covers[0]) > 3 else ""
    m = re.search(NUM + r"\s*分", full)
    if not m:
        msgs.append(f"\\examcover 第 4 参数未写明满分: {full!r}")
        return msgs
    expected = float(m.group(1))

    # 以 \parttitle 为界切分，逐段统计，避免"部分小计"与"题型小计"重复累加
    marks = [mm.start() for mm in re.finditer(r"\\parttitle", text)]
    segments = []
    if marks:
        for i, start in enumerate(marks):
            end = marks[i + 1] if i + 1 < len(marks) else len(text)
            segments.append(text[start:end])
    else:
        segments.append(text)

    total = 0.0
    detail: list[str] = []
    for seg in segments:
        seg_total = 0.0
        pt = arg_groups(seg, r"\parttitle")
        pt_score = scores_in(pt[0][0]) if pt else 0.0

        qts = []
        for m2 in re.finditer(r"\\qtypename", seg):
            parsed = arg_groups(seg[m2.start():m2.start() + 400], r"\qtypename")
            if parsed:
                qts.append(parsed[0])
        if qts:
            qt_total = 0.0
            for args in qts:
                s = scores_in(args[1] if len(args) > 1 else "")
                detail.append(f"  qtypename {args[0][:16]!r} -> {s:g}")
                qt_total += s
            seg_total = qt_total
            if pt_score and abs(pt_score - qt_total) > 1e-6:
                detail.append(f"  !! 分段小计不符: parttitle {pt_score:g} vs 题型合计 {qt_total:g}")
        elif pt_score:
            detail.append(f"  parttitle {pt[0][0][:28]!r} -> {pt_score:g}")
            seg_total = pt_score
        total += seg_total

    msgs.extend(detail)
    if abs(total - expected) > 1e-6:
        msgs.insert(0, f"分值不符: 各题型合计 {total:g} 分, 封面写 {expected:g} 分")
    # 题目数量统计
    nq = len(re.findall(r"(?<!\\)\\q(?![a-zA-Z])", text))
    npq = len(re.findall(r"\\pq(?![a-zA-Z])", text))
    msgs.append(f"OK  {expected:g} 分, 普通题 {nq} 道" + (f", 编程题 {npq} 道" if npq else ""))
    return msgs


def main() -> int:
    pats = sys.argv[1:]
    bad = 0
    checked = 0
    for p in sorted(ROOT.rglob("mock-exam-*.tex")):
        rel = str(p.relative_to(ROOT))
        if any(s in rel for s in ("tmp/", "out/", ".kilo/", ".git/")):
            continue
        if pats and not any(q in rel for q in pats):
            continue
        raw = p.read_text(encoding="utf-8")
        if "\\examcover" not in raw:
            continue          # 旧版卷子，不套用新规则
        checked += 1
        res = check(p)
        head = f"[{'FAIL' if any(x.startswith(('缺少', '分值不符', '\\examcover')) for x in res) else ' ok '}] {rel}"
        print(head)
        for line in res:
            print("     " + line)
        if head.startswith("[FAIL"):
            bad += 1
    if not checked:
        print("没有找到使用 \\examcover 的试卷")
        return 0
    print(f"\n检查完成，{bad} 个文件有问题" if bad
          else f"\n检查完成，{checked} 个文件全部通过")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
