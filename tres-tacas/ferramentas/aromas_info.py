"""Vídeo de informações (ex.: a caixa Papillon) no mesmo estilo dos 'Aromas às cegas':
título e lista do que vem na caixa numa coluna lateral, itens entrando conforme ela fala, um bloco de exemplo
(aromas do Malbec) que aparece e some, 'tim' baixinho a cada item e cartão final.

uso: python3 aromas_info.py info_v2.json pasta_saida [lado=direita|esquerda]
"""
import os, sys, json, subprocess, wave
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual as V

P = json.load(open(sys.argv[1])); OUTD = sys.argv[2]; os.makedirs(OUTD, exist_ok=True)
LADO = sys.argv[3] if len(sys.argv) > 3 else "direita"
VID = P["video"]; W, H, FPS = 1080, 1920, 30
X = W - 130 if LADO == "direita" else 130; ANC = "r" if LADO == "direita" else "l"
FADE, HI, END = 6, 1.4, 2.6
GREEN = (172, 200, 150)

def spaced(d, x, y, txt, font, fill, anchor="lm", track=3):
    w = sum(font.getlength(c) for c in txt) + track * (len(txt) - 1)
    x0 = x - w if anchor[0] == "r" else (x - w / 2 if anchor[0] == "m" else x)
    for c in txt: d.text((x0, y), c, font=font, fill=fill, anchor="l" + anchor[1]); x0 += font.getlength(c) + track

def estado(t):
    itens, malbec, novo, tn = [], False, None, -99
    for e in P["rodada1"]:
        if e[0] > t: break
        if e[1] == "item": itens.append(e[2]); novo, tn = e[2], e[0]
        elif e[1] == "malbec_on": malbec = True
        elif e[1] == "malbec_off": malbec = False
    return itens, malbec, novo, tn

def overlay(itens, malbec, novo, fade, hi, mfade):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    sh = np.zeros((H, W, 4), np.uint8); x0, x1 = (W - 560, W) if LADO == "direita" else (0, 560)
    g = np.linspace(0, 1, x1 - x0) if LADO == "direita" else np.linspace(1, 0, x1 - x0)
    a = (np.clip(g * 1.5, 0, 1) * 110).astype(np.uint8)
    yy = np.ones(H); yy[:160] = 0; yy[160:240] = np.linspace(0, 1, 80); yy[1260:] = 0; yy[1180:1260] = np.linspace(1, 0, 80)
    sh[:, x0:x1, 3] = (a[None, :] * yy[:, None]).astype(np.uint8); sh[:, x0:x1, :3] = (12, 6, 9)
    im.alpha_composite(Image.fromarray(sh))
    an = ANC + "m"
    d.text((X, 300), P["titulo"], font=V.font("dmserif", 80), fill=V.CHAMPAGNE + (255,), anchor=an)
    d.text((X, 368), P.get("sub", ""), font=V.font("dmserif_it", 42), fill=V.CREAM + (235,), anchor=an)
    spaced(d, X, 470, "NA CAIXA", V.font("jost500", 22), GREEN + (245,), an, 4)
    f = V.font("jost400", 33)
    for k, nm in enumerate(itens):
        isn = nm == novo; al = int(255 * (fade if isn else 1)); c = V.CHAMPAGNE if (isn and hi) else V.CREAM
        dx = int((1 - fade) * 24) * (-1 if LADO == "direita" else 1) if isn else 0
        d.text((X + dx, 525 + k * 46), nm, font=f, fill=c + (al,), anchor=an)
    if mfade > 0:
        y = 525 + len(itens) * 46 + 50; al = int(255 * mfade)
        spaced(d, X, y, "NO MALBEC, SEGUNDO A CAIXA", V.font("jost500", 20), V.LINE + (al,), an, 3)
        for k, ln in enumerate(("ameixa · cereja · figo", "goiaba · jabuticaba", "morango · violeta")):
            d.text((X, y + 46 + k * 40), ln, font=V.font("dmserif_it", 34), fill=V.CREAM + (al,), anchor=an)
    return np.array(V.shadowed(im, 6, 200))

def cartao(linhas):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im); y = 780; prev = 0
    for txt, k, sz in linhas:
        cor = V.CHAMPAGNE if k == "dmserif" else (V.LINE if k == "jost500" else V.CREAM)
        y += int(prev * 0.75 + sz * 0.75) if prev else 0; prev = sz
        if k == "jost500": spaced(d, W // 2, y, txt, V.font(k, sz), cor + (255,), "mm", 5)
        else: d.text((W // 2, y), txt, font=V.font(k, sz), fill=cor + (255,), anchor="mm")
    return np.array(V.shadowed(im, 12, 200))

def sons(total, path, sr=48000):
    y = np.zeros(int((total + 2) * sr), np.float32); t = np.arange(int(0.7 * sr)) / sr
    env = lambda dec: np.exp(-t / dec) * np.minimum(1, t / 0.004)
    tim = 0.6 * (0.040 * env(0.16) * np.sin(2 * np.pi * 1568 * t) + 0.028 * env(0.12) * np.sin(2 * np.pi * 2093 * t))
    for e in P["rodada1"]:
        if e[1] == "item":
            i = int(e[0] * sr); m = max(0, min(len(tim), len(y) - i)); y[i:i + m] += tim[:m]
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def main():
    dur = min(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VID],
                                   capture_output=True, text=True).stdout), P["fim_rodada1"] + 0.3)
    out = f"{OUTD}/papillon.mp4"; sons(dur + END, f"{OUTD}/sons.wav")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", VID, "-i", f"{OUTD}/sons.wav", "-filter_complex",
                            f"[1:a]afade=t=out:st={dur - 0.3:.2f}:d=0.3,apad[v];[2:a]aresample=48000[s];[v][s]amix=inputs=2:normalize=0:duration=longest[a]",
                            "-map", "0:v", "-map", "[a]", "-t", f"{dur + END:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", VID, "-t", f"{dur:.3f}", "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo",
                            "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    mon = [e[0] for e in P["rodada1"] if e[1] == "malbec_on"]; moff = [e[0] for e in P["rodada1"] if e[1] == "malbec_off"]
    cache = {}; n = 0; last = None; fs = W * H * 3
    while True:
        raw = dec.stdout.read(fs)
        if len(raw) < fs: break
        t = n / FPS; fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
        itens, malbec, novo, tn = estado(t); age = t - tn; fst = min(FADE, int(age * FPS))
        mf = 0.0
        for a, b in zip(mon, moff + [1e9] * (len(mon) - len(moff))):
            if a <= t < b + 0.3: mf = min(1, (t - a) * 4, max(0, (b + 0.3 - t) * 4))
        key = (len(itens), fst, age < HI, round(mf, 1))
        if key not in cache:
            if len(cache) > 40: cache.clear()
            cache[key] = overlay(itens, malbec, novo, fst / FADE if fst < FADE else 1.0, age < HI, round(mf, 1))
        V.over(fr, cache[key], 0, 0); enc.stdin.write(fr.tobytes()); last = fr; n += 1
    dec.wait()
    card = cartao([tuple(x) for x in P["fim"]]); b = cv2.GaussianBlur(last, (0, 0), 20)
    for k in range(int(END * FPS)):
        pr = min(1, k / 10); f2 = (b.astype(np.float32) * (1 - 0.6 * pr)).astype(np.uint8)
        c = card.copy(); c[..., 3] = (c[..., 3] * pr).astype(np.uint8); V.over(f2, c, 0, 0); enc.stdin.write(f2.tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "6", "-i", out, "-frames:v", "1", "-vf", "scale=432:-2", f"{OUTD}/papillon_capa.jpg"], check=True)
    print("ok", out, round(dur + END, 1), flush=True)

if __name__ == "__main__": main()
