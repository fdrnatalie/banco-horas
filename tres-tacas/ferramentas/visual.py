"""Identidade visual da série Três Taças: cores, fontes, fundo, painéis, cartões e legendas (1920x1080)."""
import os, textwrap
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
OX = (23, 7, 9); AMBER = (227, 145, 60); CREAM = (244, 235, 226); GOLD = (200, 164, 108)
_F = {}
FONT_FILES = {"osw600": "osw600.woff", "osw500": "osw500.woff", "corm_it600": "corm_it600.woff", "corm_it500": "corm_it500.woff",
              "corm500": "corm500.woff", "corm600": "corm600.woff", "int600": "int600.woff", "int500": "int500.woff"}
CHAMPAGNE = (232, 205, 165); LINE = (200, 164, 108)

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
    """vinho profundo, luz suave no centro, grão fino; sem molduras."""
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.42) / H) ** 2)
    c1, c2 = np.array([0x22, 0x14, 0x2c], np.float32), np.array([0x0e, 0x06, 0x12], np.float32)   # BGR
    t = np.clip(d * 1.35, 0, 1)[..., None]; bg = c1 * (1 - t) + c2 * t
    rng = np.random.default_rng(7); bg += rng.normal(0, 2.2, bg.shape[:2])[..., None]
    bg = np.clip(bg, 0, 255).astype(np.uint8)
    if label:
        im = Image.new("RGBA", (W, H)); dr = ImageDraw.Draw(im)
        dr.text((W - 64, H - 46), label.upper(), font=font("osw500", 20), fill=LINE + (170,), anchor="rm")
        over(bg, np.array(im), 0, 0)
    return bg

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
    """cartão translúcido, filete dourado fino; título em serifa, itens separados por linhas finas."""
    title = title.replace("→", "—"); lines = [l.replace("→", "—") for l in lines]
    ts = int(tsize * 0.95); ls_ = int(lsize * 0.9)
    ft, fl = font("corm600", ts), font("corm500", ls_)
    def wrap(txt, f, maxw):
        out, cur = [], ""
        for wd in txt.split():
            if cur and f.getlength(cur + " " + wd) > maxw: out.append(cur); cur = wd
            else: cur = (cur + " " + wd).strip()
        if cur: out.append(cur)
        return out
    pad = 52; inner = w - 2 * pad
    tl = wrap(title, ft, inner) if title else []
    blocks = [wrap(l, fl, inner) for l in lines]
    lh_t, lh_l, gap = int(ts * 1.12), int(ls_ * 1.3), 22
    hgt = pad + len(tl) * lh_t + (gap if tl and lines else 0) + sum(len(b) * lh_l for b in blocks) + gap * max(0, len(blocks) - 1) + pad - 6
    im = Image.new("RGBA", (w, hgt)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([1, 1, w - 2, hgt - 2], 18, fill=(14, 6, 9, 205), outline=LINE + (150,), width=2)
    y = pad + lh_t // 2 - 4
    for ln in tl: d.text((pad, y), ln, font=ft, fill=CHAMPAGNE + (255,), anchor="lm"); y += lh_t
    if tl and lines: y += gap - lh_t // 2 + lh_l // 2 - 6
    else: y += lh_l // 2 - lh_t // 2
    for k, b in enumerate(blocks):
        if k: d.line([(pad, y - lh_l // 2 - gap // 2 + 2), (pad + 60, y - lh_l // 2 - gap // 2 + 2)], fill=LINE + (110,), width=1)
        for ln in b: d.text((pad, y), ln, font=fl, fill=CREAM + (240,), anchor="lm"); y += lh_l
        y += gap
    return np.array(shadowed(im, 16, 120))

def chapter_banner(n, title, sub):
    im = Image.new("RGBA", (1100, 200)); d = ImageDraw.Draw(im)
    d.text((2, 34), f"CAPÍTULO {n:02d}", font=font("osw500", 24), fill=LINE + (230,), anchor="lm")
    d.line([(2, 58), (70, 58)], fill=LINE + (160,), width=1)
    d.text((0, 112), title, font=font("corm600", 76), fill=CHAMPAGNE + (255,), anchor="lm")
    if sub: d.text((2, 168), sub, font=font("corm_it500", 40), fill=CREAM + (225,), anchor="lm")
    return np.array(shadowed(im, 14, 190))

def cover(series, title, sub):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    d.text((104, 330), series.upper(), font=font("osw500", 30), fill=LINE + (235,), anchor="lm")
    d.line([(104, 362), (190, 362)], fill=LINE + (170,), width=1)
    d.text((98, 450), title, font=font("corm600", 112), fill=CHAMPAGNE + (255,), anchor="lm")
    d.text((104, 560), sub, font=font("corm_it500", 58), fill=CREAM + (230,), anchor="lm")
    return np.array(shadowed(im, 14, 170))

def end_card(series, cta):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    d.text((W / 2, 330), series.upper(), font=font("osw500", 30), fill=LINE + (235,), anchor="mm")
    d.text((W / 2, 460), "obrigada por provar comigo", font=font("corm_it500", 90), fill=CREAM + (245,), anchor="mm")
    d.text((W / 2, 600), "Até a próxima prova", font=font("corm600", 108), fill=CHAMPAGNE + (255,), anchor="mm")
    d.text((W / 2, 740), cta, font=font("corm_it500", 44), fill=CREAM + (225,), anchor="mm")
    return np.array(shadowed(im, 14, 170))

def caption(words, emph=(), size=46, maxw=1500):
    """uma linha de legenda: Inter médio, creme, sombra suave; destaque em champanhe."""
    f = font("int500", size); sp = f.getlength(" ")
    widths = [f.getlength(w) for w in words]; tw = sum(widths) + sp * (len(words) - 1)
    im = Image.new("RGBA", (int(min(tw, maxw)) + 40, size + 34)); d = ImageDraw.Draw(im); x = 20
    for w, wd in zip(words, widths):
        core = w.lower().strip(".,!?…;:\"'")
        d.text((x, (size + 34) // 2), w, font=f, fill=(CHAMPAGNE if core in emph else CREAM) + (255,), anchor="lm"); x += wd + sp
    return np.array(shadowed(im, 7, 210))
