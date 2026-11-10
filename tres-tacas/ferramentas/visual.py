"""Identidade visual da série Três Taças: cores, fontes, fundo, painéis, cartões e legendas (1920x1080)."""
import os, textwrap
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
OX = (23, 7, 9); AMBER = (227, 145, 60); CREAM = (244, 235, 226); GOLD = (200, 164, 108)
_F = {}
FONT_FILES = {"osw600": "osw600.woff", "corm_it600": "corm_it600.woff", "corm500": "corm500.woff", "int600": "int600.woff"}

def font(k, size):
    if (k, size) not in _F: _F[(k, size)] = ImageFont.truetype(os.path.join(HERE, "fontes", FONT_FILES[k]), size)
    return _F[(k, size)]

def shadowed(im, blur=8, alpha=180):
    """RGBA image with a soft dark shadow behind its opaque pixels."""
    a = np.array(im)[..., 3]
    sh = Image.fromarray(a).filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.putalpha(sh.point(lambda v: int(v * alpha / 255)))
    out.alpha_composite(im)
    return out

def over(dst, rgba, x, y):
    """alpha-composite an RGBA numpy image onto a BGR frame at (x, y), clipped to the frame."""
    h, w = rgba.shape[:2]; H_, W_ = dst.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W_, x + w), min(H_, y + h)
    if x0 >= x1 or y0 >= y1: return
    s = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4].astype(np.float32) / 255
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (d * (1 - a) + s[..., 2::-1].astype(np.float32) * a).astype(np.uint8)

def background(label):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W * 0.55) / W) ** 2 + ((yy - H * 0.4) / H) ** 2)
    c1, c2 = np.array([0x22, 0x12, 0x46], np.float32), np.array(OX[::-1], np.float32)
    t = np.clip(d * 1.5, 0, 1)[..., None]; bg = (c1 * (1 - t) + c2 * t).astype(np.uint8)
    im = Image.new("RGBA", (W, H)); dr = ImageDraw.Draw(im); g = GOLD + (150,)
    dr.rectangle([26, 26, W - 26, H - 26], outline=GOLD + (60,), width=2)
    for (x, y, sx, sy) in [(18, 18, 1, 1), (W - 18, 18, -1, 1), (18, H - 18, 1, -1), (W - 18, H - 18, -1, -1)]:
        dr.line([(x, y), (x + sx * 40, y)], fill=g, width=3); dr.line([(x, y), (x, y + sy * 40)], fill=g, width=3)
    dr.text((W - 60, H - 50), label, font=font("osw600", 24), fill=GOLD + (200,), anchor="rm")
    over(bg, np.array(im), 0, 0); return bg

def rounded(img_rgb, r=22, border=True):
    """RGB numpy -> RGBA numpy with rounded corners, gold border and shadow margin m; returns (rgba, m)."""
    h, w = img_rgb.shape[:2]; m = 16
    im = Image.new("RGBA", (w + 2 * m, h + 2 * m))
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    tile = Image.fromarray(img_rgb).convert("RGBA"); tile.putalpha(mask)
    im.alpha_composite(tile, (m, m))
    if border: ImageDraw.Draw(im).rounded_rectangle([m, m, m + w - 1, m + h - 1], r, outline=GOLD + (230,), width=3)
    return np.array(shadowed(im, 10, 170)), m

def card(w, title, lines, tsize=64, lsize=46, bullet=True):
    """dark card with an amber title and cream italic lines; height fits the content."""
    title = title.replace("→", "—"); lines = [l.replace("→", "—") for l in lines]
    tl = textwrap.wrap(title, max(8, int((w - 112) / (tsize * 0.47)))) if title else []
    wr = int((w - 120) / (lsize * 0.42))
    hgt = 56 + len(tl) * int(tsize * 1.15) + (20 if tl and lines else 0) + sum(len(textwrap.wrap(l, wr)) * int(lsize * 1.25) + 10 for l in lines) + 36
    im = Image.new("RGBA", (w, hgt)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w - 4, hgt - 4], 26, fill=(23, 7, 9, 235), outline=GOLD + (255,), width=3)
    y = 56 + int(tsize * 0.15)
    for ln in tl: d.text((56, y), ln, font=font("osw600", tsize), fill=AMBER + (255,), anchor="lm"); y += int(tsize * 1.15)
    if tl and lines: y += 20
    for line in lines:
        for k, ln in enumerate(textwrap.wrap(line, wr)):
            d.text((56, y), (("• " if k == 0 else "  ") if bullet else "") + ln, font=font("corm_it600", lsize), fill=CREAM + (255,), anchor="lm")
            y += int(lsize * 1.25)
        y += 10
    return np.array(shadowed(im, 12, 200))

def chapter_banner(n, title, sub):
    im = Image.new("RGBA", (1100, 190)); d = ImageDraw.Draw(im)
    for i in range(190): d.line([(0, i), (1100, i)], fill=(18, 6, 8, int(170 * min(1, i / 40))))
    d.text((0, 30), f"CAPÍTULO {n}", font=font("osw600", 30), fill=GOLD + (255,), anchor="lm")
    d.text((0, 100), title.upper(), font=font("osw600", 78), fill=AMBER + (255,), anchor="lm")
    d.text((4, 162), sub, font=font("corm_it600", 44), fill=CREAM + (255,), anchor="lm")
    return np.array(shadowed(im, 12, 200))

def cover(series, title, sub):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    d.text((100, 330), series.upper(), font=font("osw600", 44), fill=GOLD + (255,), anchor="lm")
    d.text((96, 450), title.upper(), font=font("osw600", 110), fill=AMBER + (255,), anchor="lm")
    d.text((100, 570), sub, font=font("corm_it600", 64), fill=CREAM + (255,), anchor="lm")
    return np.array(shadowed(im, 10, 180))

def end_card(series, cta):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    d.text((W / 2, 300), series, font=font("osw600", 40), fill=GOLD + (255,), anchor="mm")
    d.text((W / 2, 440), "obrigada por provar comigo", font=font("corm_it600", 96), fill=CREAM + (255,), anchor="mm")
    d.text((W / 2, 600), "ATÉ A PRÓXIMA PROVA", font=font("osw600", 120), fill=AMBER + (255,), anchor="mm")
    d.text((W / 2, 760), cta, font=font("corm_it600", 44), fill=CREAM + (255,), anchor="mm")
    return np.array(shadowed(im, 12, 180))

def caption(words, emph=(), size=46, maxw=1500):
    """one caption line (list of words) as RGBA; emphasised words in amber."""
    f = font("int600", size); sp = f.getlength(" ")
    widths = [f.getlength(w) for w in words]; tw = sum(widths) + sp * (len(words) - 1)
    im = Image.new("RGBA", (int(min(tw, maxw)) + 40, size + 30)); d = ImageDraw.Draw(im); x = 20
    for w, wd in zip(words, widths):
        core = w.lower().strip(".,!?…;:\"'")
        d.text((x, (size + 30) // 2), w, font=f, fill=(AMBER if core in emph else CREAM) + (255,), anchor="lm"); x += wd + sp
    return np.array(shadowed(im, 6, 230))
