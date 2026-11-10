"""storyboard mock frames for a roteiro: python3 mock.py roteiro.json video.mov series outdir
one jpg per tela (and one per block without telas), drawn with the video's own look."""
import os, sys, json, subprocess, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
from PIL import Image, ImageDraw
import render as RD, render_yt as Y, pip as PIP

R, VID, SERIES, OUT = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
SX0, SY0, SX1, SY1 = 0, 40, 1512, 1050
PH_ = 880; PW_ = int(PH_ * (SX1 - SX0) / (SY1 - SY0)); PX = (W - PW_) // 2; PY = 36
SIZES = [(598, 449), (520, 390), (450, 338), (400, 300), (350, 262), (300, 225), (280, 210)]

def grab(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", VID, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE).stdout
    return np.frombuffer(raw, np.uint8)[:1512 * 1050 * 3].reshape(1050, 1512, 3)

def face(fr, w, h):
    x, y, fw, fh = PIP.locate_multi(fr, SIZES)
    c = PIP.face_crop(fr, x, y, 6, w / h, fw, fh)
    return cv2.resize(c, (w, h), interpolation=cv2.INTER_AREA)

def put(bg, img_bgr, x, y, r=24):
    p, m = Y.rounded_panel(img_bgr[..., ::-1], r=r); Y.over(bg, p, x - m, y - m)

def caption(bg, text):
    if not text: return
    words = text.split(); text = " ".join(words[:9]) + (" …" if len(words) > 9 else "")
    im = Image.new("RGBA", (W, 90)); d = ImageDraw.Draw(im)
    d.text((W // 2, 45), text, font=RD.font("inter600", 40) if "inter600" in RD.FONTS else RD.font("osw600", 40), fill=RD.CREAM + (255,), anchor="mm")
    Y.over(bg, np.array(RD.shadowed(im, 6, 220)), 0, 955)

def card(w, h, title, lines, tsize=64, lsize=46):
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w - 4, h - 4], 26, fill=(23, 7, 9, 235), outline=RD.GOLD + (255,), width=3)
    y = 70; ft = RD.font("osw600", tsize)
    for ln in textwrap.wrap(title, 30 if tsize <= 64 else 24):
        d.text((56, y), ln, font=ft, fill=RD.AMBER + (255,), anchor="lm"); y += int(tsize * 1.15)
    y += 24; fl = RD.font("corm_it600", lsize)
    for line in lines:
        for k, ln in enumerate(textwrap.wrap(line, int((w - 120) / (lsize * 0.42)))):
            d.text((56, y), ("• " if k == 0 else "  ") + ln, font=fl, fill=RD.CREAM + (255,), anchor="lm"); y += int(lsize * 1.25)
        y += 10
    return np.array(im)

def render(tela, t, fala_txt):
    bg = Y.background(SERIES); fr = grab(t); tipo = tela.get("tipo", "app") if tela else "app"
    if tipo == "app" or not tela:
        sc = cv2.resize(PIP.clean_watermark(fr)[SY0:SY1, SX0:SX1], (PW_, PH_), interpolation=cv2.INTER_AREA)
        put(bg, sc, PX, PY)
        if tela and (tela.get("titulo") or tela.get("linhas")):
            Y.over(bg, card(1100, 190, tela.get("titulo", ""), tela.get("linhas", [])[:1], 46, 40), PX + 40, PY + 40)
    elif tipo in ("aula", "placar"):
        Y.over(bg, card(1060, 860, tela.get("titulo", ""), tela.get("linhas", [])), 90, 70)
        put(bg, face(fr, 640, 480), 1200, 260, r=28)
    elif tipo == "comparacao":
        im = Image.new("RGBA", (W, 130)); d = ImageDraw.Draw(im)
        d.text((100, 65), tela.get("titulo", "").upper(), font=RD.font("osw600", 64), fill=RD.AMBER + (255,), anchor="lm")
        Y.over(bg, np.array(im), 0, 50)
        cols = tela.get("linhas", []); n = max(1, len(cols)); cw = (1300 - 30 * (n - 1)) // n
        for i, c in enumerate(cols):
            head, _, body = c.partition(":")
            Y.over(bg, card(cw, 720, head.strip(), [body.strip()] if body else [], 52, 40), 90 + i * (cw + 30), 190)
        put(bg, face(fr, 400, 300), 1440, 560, r=24)
    caption(bg, fala_txt)
    return bg

for b in R["blocos"]:
    fl = b.get("falas", [])
    telas = b.get("telas") or [None]
    for k, tl in enumerate(telas):
        i = (tl or {}).get("entra_fala", 0) or 0; i = min(max(0, i), len(fl) - 1) if fl else 0
        f = fl[i] if fl else {"a": 0, "texto": ""}
        t = f["a"] + min(1.5, max(0.2, (f["b"] - f["a"]) / 2)) if fl else 0
        img = render(tl, t, f.get("texto", ""))
        cv2.imwrite(f"{OUT}/{b['id']}_{k}.jpg", cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 86])
        print(b["id"], k, tl and tl.get("tipo"), flush=True)
