from PIL import Image, ImageDraw, ImageFont
import glob, os

OUT = "/home/admin/kana-android/assets"
os.makedirs(OUT, exist_ok=True)

cands = glob.glob("/usr/share/fonts/**/NotoSansCJK*Black*", recursive=True) + \
        glob.glob("/usr/share/fonts/google-noto-cjk/*.ttc")
FONT = sorted(cands)[0]
INDIGO = (44, 62, 107, 255)
CREAM = (255, 253, 248, 255)
WASHI = (244, 239, 230, 255)

S = 2048


def glyph_layer(size, glyph_ratio, color=CREAM):
    """透明底 + 置中「あ」"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, int(size * glyph_ratio))
    bbox = d.textbbox((0, 0), "あ", font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), "あ", font=font, fill=color)
    return img


# 1) 完整圖示 1024（cap assets 用）
icon = Image.new("RGBA", (S, S), INDIGO)
d = ImageDraw.Draw(icon)
pad = int(S * 0.13)
d.ellipse([pad, pad, S - pad, S - pad], outline=(255, 255, 255, 30), width=int(S * 0.006))
r = int(S * 0.030)
d.ellipse([int(S * 0.80) - r, int(S * 0.20) - r, int(S * 0.80) + r, int(S * 0.20) + r], fill=(200, 64, 47, 255))
icon = Image.alpha_composite(icon, glyph_layer(S, 0.50))
icon.resize((1024, 1024), Image.LANCZOS).save(f"{OUT}/icon.png")

# 2) 前景層（adaptive icon，透明底，字留 66% 安全區）
fg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
fg = Image.alpha_composite(fg, glyph_layer(S, 0.36))
fg.resize((1024, 1024), Image.LANCZOS).save(f"{OUT}/icon-foreground.png")

# 3) 背景層
Image.new("RGBA", (1024, 1024), INDIGO).save(f"{OUT}/icon-background.png")

# 4) Splash 2732：和紙底 + 標誌 + 標題
W = 2732
sp = Image.new("RGB", (W, W), WASHI[:3])
mark = Image.new("RGBA", (900, 900), (0, 0, 0, 0))
dm = ImageDraw.Draw(mark)
dm.rounded_rectangle([0, 0, 899, 899], radius=200, fill=INDIGO)
dm.ellipse([117, 117, 782, 782], outline=(255, 255, 255, 30), width=5)
mark = Image.alpha_composite(mark, glyph_layer(900, 0.50))
sp.paste(mark, (int((W - 900) / 2), int(W * 0.40) - 450), mark)
sp.save(f"{OUT}/splash.png")
sp.resize((512, 512), Image.LANCZOS).save(f"{OUT}/splash-512.png")

for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    print(f, Image.open(p).size, os.path.getsize(p) // 1024, "KB")
