from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/home/admin/kana-dojo/icons"
os.makedirs(OUT, exist_ok=True)

FONT = "/usr/share/fonts/google-noto-sans-cjk-ttc-fonts/NotoSansCJK-Bold.ttc"
if not os.path.exists(FONT):
    import glob
    cands = glob.glob("/usr/share/fonts/**/NotoSansCJK*Bold*", recursive=True) + \
            glob.glob("/usr/share/fonts/**/NotoSansCJK*", recursive=True)
    FONT = sorted(cands)[0]
print("font:", FONT)

INDIGO = (44, 62, 107)
CREAM = (255, 253, 248)
VERM = (200, 64, 47)


def draw_icon(size, glyph_ratio, bg=True, vermilion_dot=True, rounded=True):
    S = size * 4  # supersample
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bg:
        if rounded:
            d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.22), fill=INDIGO)
        else:
            d.rectangle([0, 0, S - 1, S - 1], fill=INDIGO)
    # 淡色圈
    pad = int(S * 0.13)
    d.ellipse([pad, pad, S - pad, S - pad], outline=(255, 255, 255, 28), width=max(2, int(S * 0.006)))

    fsize = int(S * glyph_ratio)
    font = ImageFont.truetype(FONT, fsize)
    txt = "あ"
    bbox = d.textbbox((0, 0), txt, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (S - w) / 2 - bbox[0]
    y = (S - h) / 2 - bbox[1] - S * 0.01
    d.text((x, y), txt, font=font, fill=CREAM)

    if vermilion_dot:
        r = int(S * 0.030)
        cx, cy = int(S * 0.80), int(S * 0.20)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=VERM)

    return img.resize((size, size), Image.LANCZOS)


# 一般圖示（含圓角）
for s in (192, 512):
    draw_icon(s, 0.50).save(f"{OUT}/icon-{s}.png")
# maskable：滿版背景、字細啲（安全區 80%）
draw_icon(512, 0.44, rounded=False).save(f"{OUT}/icon-maskable-512.png")
# Apple touch icon（唔透明、圓角由系統加）
draw_icon(180, 0.50, rounded=False).save(f"{OUT}/apple-touch-icon.png")
# favicon
draw_icon(32, 0.62, rounded=False).save(f"{OUT}/favicon-32.png")

for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    im = Image.open(p)
    print(f, im.size, os.path.getsize(p), "bytes")
