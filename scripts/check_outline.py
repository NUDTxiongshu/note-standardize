# -*- coding: utf-8 -*-
"""检查大纲产出是否达标。用法: python check_outline.py <note.md> [--source-chars N]"""
import io, re, sys

def check(path, source_chars=None):
    rows = []
    for i, l in enumerate(io.open(path, encoding="utf-8").read().split("\n"), 1):
        m = re.match(r"^([ ]*)- (.*)$", l)
        if m:
            rows.append({"line": i, "indent": len(m.group(1)), "text": m.group(2).strip()})
        elif l.strip():
            rows.append({"line": i, "indent": -1, "text": l.strip()})

    probs = []
    nodes = [r for r in rows if r["indent"] >= 0]
    body = [r for r in rows if r["indent"] > 0]
    lens = [len(r["text"]) for r in body]

    # 1 无编号行
    unnum = [r for r in nodes if r["indent"] > 0 and not re.match(r"^\d", r["text"])]
    if unnum:
        probs.append("无编号节点 %d 个，首例 L%d: %s" % (len(unnum), unnum[0]["line"], unnum[0]["text"][:40]))

    # 2 编号连续性
    prev = {}
    for r in nodes:
        if r["indent"] == 0:
            continue
        m = re.match(r"^(\d+(?:\.\d+)*)", r["text"])
        if not m:
            continue
        seg = [int(x) for x in m.group(1).split(".")]
        parent = tuple(seg[:-1])
        if parent in prev and seg[-1] != prev[parent] + 1:
            probs.append("编号跳号 L%d: %s（上一个是 .%d）" % (r["line"], m.group(1), prev[parent]))
        prev[parent] = seg[-1]

    # 3 一级分支数（根的下一层）
    l1 = [r for r in nodes if r["indent"] == 2]
    if not (2 <= len(l1) <= 5):
        probs.append("一级分支 %d 个（应 2-5）" % len(l1))

    # 4 重复概念：去掉编号后取前 6 字做 key
    seen = {}
    dups = []
    for r in nodes:
        if r["indent"] == 0:
            continue
        t = re.sub(r"^\d+(\.\d+)*\s*", "", r["text"])
        key = t[:6]
        if len(key) >= 4:
            if key in seen:
                dups.append((seen[key], r["line"], key))
            else:
                seen[key] = r["line"]
    if dups:
        probs.append("疑似重复 %d 处，首例 L%d 与 L%d: %s" % (len(dups), dups[0][0], dups[0][1], dups[0][2]))

    # 5 体量
    total = sum(lens)
    stats = {
        "节点数": len(body),
        "文字总量": total,
        "均值": total // len(body) if body else 0,
        "最长": max(lens) if lens else 0,
    }
    if not (25 <= len(body) <= 45):
        probs.append("节点数 %d（目标 25-45）" % len(body))
    if not (600 <= total <= 1200):
        probs.append("文字总量 %d（目标 600-1200）" % total)
    if lens and max(lens) > 60:
        probs.append("最长节点 %d 字（上限 60）" % max(lens))

    # 6 疑似截断：以单字词尾收束且无标点
    trunc = []
    for r in body:
        t = r["text"]
        if len(t) > 25 and re.search(r"[的一是在和用至以]$", t):
            trunc.append(r)
    if trunc:
        probs.append("疑似截断 %d 处，首例 L%d: ...%s" % (len(trunc), trunc[0]["line"], trunc[0]["text"][-20:]))

    # 7 例句痕迹
    ex = [r for r in body if re.search(r"[A-Za-z]{3,}\s+[A-Za-z]{3,}\s+[A-Za-z]{3,}", r["text"])]
    if len(ex) > 3:
        probs.append("疑似含完整英文例句 %d 处，首例 L%d" % (len(ex), ex[0]["line"]))

    return stats, probs

if __name__ == "__main__":
    path = sys.argv[1]
    stats, probs = check(path)
    print("=== 统计 ===")
    for k, v in stats.items():
        print("  %s: %s" % (k, v))
    print("=== 问题 %d 处 ===" % len(probs))
    for p in probs:
        print("  ! " + p)
    if not probs:
        print("  通过")