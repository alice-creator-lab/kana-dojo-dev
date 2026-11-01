#!/usr/bin/env python3
"""由 46 清音筆順模板合成 濁音／半濁音／拗音 嘅模板。

KanjiVG 只有 46 平假名 + 46 片假名。呢個 script 用合成方式補齊：

- 濁音（が ざ だ ば）：原本字 + 兩點（゛）
- 半濁音（ぱ ぴ ぷ ぺ ぽ）：原本字 + 一個小圈（゜）
- 拗音（きゃ しゃ …）：大字 + 縮細嘅や／ゆ／よ 放右下

座標系同 index.html 一致：單位方格、置中、n 點重取樣。

用法：
  python3 tools/make_extra_templates.py            # 寫入 kana-templates.json
  python3 tools/make_extra_templates.py --dry-run  # 只印統計
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, "kana-templates.json")

# ── 規則表（同 index.html 嘅 DAKU/HAND/YOUON 對齊）────────────────
DAKU = {
    "が": "か", "ぎ": "き", "ぐ": "く", "げ": "け", "ご": "こ",
    "ざ": "さ", "じ": "し", "ず": "す", "ぜ": "せ", "ぞ": "そ",
    "だ": "た", "ぢ": "ち", "づ": "つ", "で": "て", "ど": "と",
    "ば": "は", "び": "ひ", "ぶ": "ふ", "べ": "へ", "ぼ": "ほ",
}
DAKU_KATA = {
    "ガ": "カ", "ギ": "キ", "グ": "ク", "ゲ": "ケ", "ゴ": "コ",
    "ザ": "サ", "ジ": "シ", "ズ": "ス", "ゼ": "セ", "ゾ": "ソ",
    "ダ": "タ", "ヂ": "チ", "ヅ": "ツ", "デ": "テ", "ド": "ト",
    "バ": "ハ", "ビ": "ヒ", "ブ": "フ", "ベ": "ヘ", "ボ": "ホ",
}
HAND = {"ぱ": "は", "ぴ": "ひ", "ぷ": "ふ", "ぺ": "へ", "ぽ": "ほ"}
HAND_KATA = {"パ": "ハ", "ピ": "ヒ", "プ": "フ", "ペ": "ヘ", "ポ": "ホ"}

# 拗音：大字 + 細字（細字用番大楷模板縮細）
YOUON_PAIRS = [
    ("き", "や"), ("し", "や"), ("ち", "や"), ("に", "や"), ("ひ", "や"),
    ("み", "や"), ("り", "や"), ("ぎ", "や"), ("じ", "や"), ("び", "や"), ("ぴ", "や"),
    ("き", "ゆ"), ("し", "ゆ"), ("ち", "ゆ"), ("に", "ゆ"), ("ひ", "ゆ"),
    ("み", "ゆ"), ("り", "ゆ"), ("ぎ", "ゆ"), ("じ", "ゆ"), ("び", "ゆ"), ("ぴ", "ゆ"),
    ("き", "よ"), ("し", "よ"), ("ち", "よ"), ("に", "よ"), ("ひ", "よ"),
    ("み", "よ"), ("り", "よ"), ("ぎ", "よ"), ("じ", "よ"), ("び", "よ"), ("ぴ", "よ"),
]
def to_kata(s):
    """平假名 → 片假名（Unicode 偏移 +0x60，連濁音／半濁音都覆蓋）"""
    return "".join(chr(ord(c) + 0x60) if 0x3041 <= ord(c) <= 0x3096 else c for c in s)
# 拗音用細寫假名（字形同大寫一樣，只係細啲）
SMALL_MAP = {"や": "ゃ", "ゆ": "ゅ", "よ": "ょ", "ヤ": "ャ", "ユ": "ュ", "ヨ": "ョ"}


def normalize(strokes):
    xs = [p[0] for s in strokes for p in s]
    ys = [p[1] for s in strokes for p in s]
    side = max(max(xs) - min(xs), max(ys) - min(ys), 1e-9)
    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    return [[((x - cx) / side, (y - cy) / side) for x, y in s] for s in strokes]


def place(strokes, scale, dx, dy):
    return [[(x * scale + dx, y * scale + dy) for x, y in s] for s in strokes]


def resample(pts, n=16):
    if len(pts) < 2:
        return [tuple(pts[0])] * n
    d = [0.0]
    for i in range(1, len(pts)):
        d.append(d[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    total = d[-1]
    if total <= 0:
        return [tuple(pts[0])] * n
    out, j = [], 0
    for k in range(n):
        tgt = total * k / (n - 1)
        while j < len(d) - 2 and d[j + 1] < tgt:
            j += 1
        seg = d[j + 1] - d[j]
        t = (tgt - d[j]) / seg if seg else 0.0
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t,
                    pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t))
    return out


def line(a, b, steps=8):
    return [(a[0] + (b[0] - a[0]) * i / steps, a[1] + (b[1] - a[1]) * i / steps) for i in range(steps + 1)]


def circle(cx, cy, r, steps=16):
    pts = []
    for i in range(steps):
        a = 2 * math.pi * i / steps
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    return pts


# 濁點：右上角兩筆短撇（寫法：左上→右下）
DAKUTEN = [line((0.14, -0.46), (0.30, -0.32)), line((0.33, -0.44), (0.48, -0.30))]
# 半濁點：右上角一個小圈
HANDAKUTEN = [circle(0.34, -0.37, 0.085)]


def build(tpl):
    out = {}
    missing = []
    pairs = list(DAKU.items()) + list(DAKU_KATA.items())

    for ch, base in pairs:
        if base not in tpl:
            missing.append(base)
            continue
        strokes = place(tpl[base], 0.74, -0.13, 0.02) + [list(s) for s in DAKUTEN]
        out[ch] = normalize(strokes)

    for ch, base in list(HAND.items()) + list(HAND_KATA.items()):
        if base not in tpl:
            missing.append(base)
            continue
        strokes = place(tpl[base], 0.74, -0.13, 0.02) + [list(s) for s in HANDAKUTEN]
        out[ch] = normalize(strokes)

    for big, small in YOUON_PAIRS:
        for a, b in ((big, small), (to_kata(big), to_kata(small))):
            a_src = tpl.get(a) or out.get(a)          # ぎゃ 嘅「ぎ」係合成出嚟
            b_src = tpl.get(b)
            if a_src is None:
                missing.append(a)
                continue
            if b_src is None:
                missing.append(b)
                continue
            strokes = place(a_src, 0.62, -0.20, 0.0) + place(b_src, 0.34, 0.30, 0.26)
            out[a + SMALL_MAP.get(b, b)] = normalize(strokes)

    return out, missing


def main():
    dry = "--dry-run" in sys.argv
    data = json.load(open(JSON_PATH, encoding="utf-8"))
    tpl = data["tpl"]
    extra, missing = build(tpl)

    print(f"原有模板：{len(tpl)}")
    print(f"新增模板：{len(extra)}  (濁音 {len(DAKU)+len(DAKU_KATA)}, "
          f"半濁音 {len(HAND)+len(HAND_KATA)}, 拗音 {len(YOUON_PAIRS)*2})")
    if missing:
        print("⚠ 缺少基礎模板：", sorted(set(missing)))
    added = [k for k in extra if k not in tpl]
    print(f"實際新增：{len(added)} 個 →", "".join(added[:12]), "…")

    if dry:
        return

    tpl.update(extra)
    # 保持原格式：緊湊、3 位小數
    def r3(v):
        return round(float(v), 3) + 0.0

    for k in added:
        tpl[k] = [[[r3(x), r3(y)] for x, y in resample(s, 16)] for s in tpl[k]]
    text = json.dumps({"n": data.get("n", 16), "tpl": tpl}, ensure_ascii=False, separators=(",", ":"))
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"已寫入 {JSON_PATH}（{len(tpl)} 模板，{os.path.getsize(JSON_PATH) / 1024:.0f} KB）")


if __name__ == "__main__":
    main()
