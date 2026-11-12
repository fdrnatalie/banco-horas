"""Reels/Shorts verticais (1080x1920) a partir de blocos de um roteiro por temas.

uso: python3 montar_reels.py spec.json
spec.json: {"roteiro": ".../roteiro.json", "blocos": ["B10"] ou [{"bloco": "B10", "falas": [0, 1, 2]}],
            "gancho": "título grande do topo", "saida": ".../reels_x.mp4", "fim": "episódio completo no YouTube"}
Layout: topo = série + gancho; meio-alto = contexto (cartão da tela ou o app); meio-baixo = rosto; base = legenda.
A legenda nunca cobre o rosto. Fala a 1,1x, sem ééé/tosse/pausa dentro das falas.
"""
import os, sys, json, subprocess, wave, re
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual as V, rosto, cleanfala

SP = json.load(open(sys.argv[1])); R = json.load(open(SP["roteiro"]))
OUT = os.path.abspath(SP["saida"]); WD = os.path.splitext(OUT)[0] + "_trab"; os.makedirs(WD, exist_ok=True)
VID = os.path.abspath(R["video"]); FPS, SPEED = 30, 1.1
W, H = 1080, 1920
CTX = (60, 330, 960, 560)            # x, y, w, h do contexto
FACE = (90, 930, 900, 675)           # janela do rosto (4:3) — nada é desenhado por cima
CAP_Y = 1745; END_S = 2.5

def sh(*a): subprocess.run(list(a), check=True)

def grab(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", VID, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE).stdout
    return np.frombuffer(raw, np.uint8)[:1512 * 1050 * 3].reshape(1050, 1512, 3) if len(raw) >= 1512 * 1050 * 3 else None

def background():
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.35) / H) ** 2)
    c1, c2 = np.array([0x22, 0x12, 0x46], np.float32), np.array(V.OX[::-1], np.float32)
    t = np.clip(d * 1.6, 0, 1)[..., None]; return (c1 * (1 - t) + c2 * t).astype(np.uint8)

def header():
    im = Image.new("RGBA", (W, 300)); d = ImageDraw.Draw(im)
    d.text((W // 2, 92), R["serie"], font=V.font("corm_it600", 46), fill=V.CREAM + (255,), anchor="mm")
    lines = wrap(SP["gancho"].upper(), V.font("osw600", 96), W - 120)
    y = 190 if len(lines) == 1 else 165
    for ln in lines[:2]: d.text((W // 2, y), ln, font=V.font("osw600", 96), fill=V.AMBER + (255,), anchor="mm"); y += 104
    return np.array(V.shadowed(im, 10, 200))

def wrap(txt, f, maxw):
    out, cur = [], ""
    for w in txt.split():
        if cur and f.getlength(cur + " " + w) > maxw: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out

def ctx_layer(tela):
    if tela is None or tela.get("tipo") == "app" and not (tela.get("titulo") or tela.get("linhas")): return None
    tipo = tela.get("tipo"); tt = tela.get("titulo", ""); ll = tela.get("linhas", [])
    if tt.lower() == "capa": return None
    if tipo == "comparacao":
        ll = [" · ".join(x.strip() for x in re.split(r" · |;", c)) for c in ll]
    return V.card(CTX[2], tt, ll[:4], 58, 40)

def pecas():
    blocos = {b["id"]: b for b in R["blocos"]}
    wav48 = f"{WD}/fonte48.wav"
    if not os.path.exists(wav48): sh("ffmpeg", "-v", "error", "-y", "-i", VID, "-vn", "-ac", "1", "-ar", "48000", wav48)
    C = cleanfala.Cleaner(R["trans"], R["hesit"], wav48)
    out = []
    for item in SP["blocos"]:
        bid, sel = (item, None) if isinstance(item, str) else (item["bloco"], item.get("falas"))
        b = blocos[bid]; telas = b.get("telas", [])
        for fi, f in enumerate(b["falas"]):
            if sel is not None and fi not in sel: continue
            tela = None
            for t in telas:
                e = t.get("entra_fala", 0) or 0; s = t.get("sai_fala", len(b["falas"]) - 1)
                if s is None: s = len(b["falas"]) - 1
                if e <= fi <= s: tela = t
            sub, _ = C.clean(f["a"], f["b"])
            for a, bb in sub: out.append(dict(a=a, b=bb, tela=tela))
    t = 0.0
    for p in out: p["o0"] = t; t += (p["b"] - p["a"]) / SPEED; p["o1"] = t
    return out, t + END_S, wav48

def audio(ps, total, wav48):
    w = wave.open(wav48); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs = []; f = int(0.012 * sr)
    for p in ps:
        seg = x[int(p["a"] * sr):int(p["b"] * sr)].copy(); lv = np.percentile(np.abs(seg), 97) if len(seg) else 0
        if lv > 1e-4: seg *= float(np.clip(0.30 / lv, 0.5, 8.0))
        if len(seg) > 2 * f: seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        segs.append(seg)
    wr(f"{WD}/voz_1x.wav", np.concatenate(segs), sr)
    chain = ("highpass=f=75,lowpass=f=14000,afftdn=nr=10:nf=-40,acompressor=threshold=0.08:ratio=3:attack=8:release=120:makeup=2,"
             f"loudnorm=I=-14:TP=-1.5:LRA=8,atempo={SPEED}")
    sh("ffmpeg", "-v", "error", "-y", "-i", f"{WD}/voz_1x.wav", "-af", chain, "-ar", "48000", "-ac", "1", f"{WD}/voz.wav")
    w2 = wave.open(f"{WD}/voz.wav"); vv = np.frombuffer(w2.readframes(w2.getnframes()), np.int16).astype(np.float32) / 32768
    mix = np.zeros(int(total * 48000), np.float32); mix[:min(len(vv), len(mix))] = vv[:len(mix)]
    wr(f"{WD}/mix.wav", mix, 48000)

def wr(path, x, sr):
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def legendas():
    from faster_whisper import WhisperModel
    import scipy.signal as ss
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    w = wave.open(f"{WD}/voz.wav"); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(ss.resample_poly(x, 1, 3).astype(np.float32), language="pt", word_timestamps=True, vad_filter=False)
    words = [[ww.word.strip(), ww.start, ww.end] for s in segs for ww in s.words if ww.word.strip(".,!?…;: ")]
    fix = {k.lower(): v for k, v in R.get("fix", {}).items()}
    for wd in words:
        core = wd[0].strip(".,!?…;:")
        if core.lower() in fix: wd[0] = wd[0].replace(core, fix[core.lower()])
    for a, b in R.get("frases_fix", []):
        aw = a.lower().split(); i = 0
        while i <= len(words) - len(aw):
            if [x_[0].lower().strip(".,!?…;:") for x_ in words[i:i + len(aw)]] == aw:
                bw = b.split(); t0, t1 = words[i][1], words[i + len(aw) - 1][2]; dd = (t1 - t0) / len(bw)
                words[i:i + len(aw)] = [[bw[k], t0 + k * dd, t0 + (k + 1) * dd] for k in range(len(bw))]; i += len(bw)
            else: i += 1
    lines, cur = [], []
    for wd in words:                                    # Reels: linhas curtas, 3-4 palavras
        if cur and (len(cur) >= 4 or len(" ".join(x_[0] for x_ in cur + [wd])) > 22 or wd[1] - cur[-1][2] > 0.6): lines.append(cur); cur = []
        cur.append(wd)
        if wd[0][-1:] in ".?!": lines.append(cur); cur = []
    if cur: lines.append(cur)
    return [(ln[0][1], min(lines[k + 1][0][1] if k + 1 < len(lines) else ln[-1][2] + 0.5, ln[-1][2] + 0.6), [x_[0] for x_ in ln])
            for k, ln in enumerate(lines)]

def main():
    ps, total, wav48 = pecas(); audio(ps, total, wav48); caps = legendas()
    emph = set(R.get("destaques", []))
    capimg = [(a, b, V.caption(t, emph, size=62, maxw=980)) for a, b, t in caps]
    bg = background(); hd = header(); cache = {}
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", f"{WD}/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    fidx = 0; last = None; box = None
    for p in ps:
        fe = int(round(p["o1"] * FPS)); n = fe - fidx
        if n <= 0: continue
        bs = [rosto.localizar(g) for g in (grab(p["a"] + (p["b"] - p["a"]) * q) for q in (0.3, 0.7)) if g is not None]
        nb = rosto.mediana(bs); box = nb or box
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{p['a']:.3f}", "-t", f"{p['b'] - p['a'] + 0.3:.3f}", "-i", VID,
                              "-vf", f"setpts=(PTS-STARTPTS)/{SPEED},fps={FPS}", "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                             stdout=subprocess.PIPE).stdout
        k_ = len(raw) // (1512 * 1050 * 3); frs = np.frombuffer(raw[:k_ * 1512 * 1050 * 3], np.uint8).reshape(k_, 1050, 1512, 3)
        if k_ == 0: frs = np.zeros((1, 1050, 1512, 3), np.uint8); k_ = 1
        if k_ < n: frs = np.concatenate([frs, np.repeat(frs[-1:], n - k_, 0)])
        key = id(p["tela"]) if p["tela"] is not None else None
        if key not in cache: cache[key] = ctx_layer(p["tela"])
        layer = cache[key]
        for k in range(n):
            t = (fidx + k) / FPS; fr = bg.copy(); src = frs[k]
            V.over(fr, hd, 0, 30)
            if layer is not None: V.over(fr, layer, CTX[0], CTX[1] + max(0, (CTX[3] - layer.shape[0]) // 2))
            else:                                       # sem cartão: mostra o app (sem a janelinha do rosto)
                app = src[40:1050].copy()
                if box: x, y, w, h = box; app[max(0, y - 40):y - 40 + h, x:x + w] = 0
                sc = cv2.resize(app, (CTX[2], int(CTX[2] * app.shape[0] / app.shape[1])), interpolation=cv2.INTER_AREA)[:CTX[3]]
                pp, m = V.rounded(sc[..., ::-1], 22); V.over(fr, pp, CTX[0] - m, CTX[1] - m)
            if box:
                fw, fh = FACE[2], FACE[3]
                if box[3] > box[2] * 1.1: fw = int(fh * 0.75)
                kk = min(1.0, 2.2 * (box[2] - 12) / fw, 2.2 * (box[3] - 12) / fh); fw2, fh2 = int(fw * kk), int(fh * kk)
                face = rosto.recorte(src, box, fw2, fh2); pp, m = V.rounded(face[..., ::-1], 30)
                V.over(fr, pp, FACE[0] + (FACE[2] - fw2) // 2 - m, FACE[1] + (FACE[3] - fh2) // 2 - m)
            for ca, cb, img in capimg:
                if ca <= t < cb: V.over(fr, img, (W - img.shape[1]) // 2, CAP_Y - img.shape[0] // 2); break
            enc.stdin.write(fr.tobytes()); last = fr
        fidx = fe
    endimg = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(endimg)
    d.text((W // 2, 820), "episódio completo", font=V.font("corm_it600", 70), fill=V.CREAM + (255,), anchor="mm")
    d.text((W // 2, 940), SP.get("fim", "NO YOUTUBE").upper(), font=V.font("osw600", 110), fill=V.AMBER + (255,), anchor="mm")
    d.text((W // 2, 1060), "link na bio", font=V.font("corm_it600", 56), fill=V.CREAM + (255,), anchor="mm")
    endimg = np.array(V.shadowed(endimg, 12, 200)); base = cv2.GaussianBlur(last, (0, 0), 18)
    for k in range(int(round(total * FPS)) - fidx):
        pr = min(1, k / 10); f2 = (base.astype(np.float32) * (1 - 0.55 * pr)).astype(np.uint8)
        e = endimg.copy(); e[..., 3] = (e[..., 3] * pr).astype(np.uint8); V.over(f2, e, 0, 0); enc.stdin.write(f2.tobytes())
    enc.stdin.close(); enc.wait()
    sh("ffmpeg", "-v", "error", "-y", "-ss", "1.5", "-i", OUT, "-frames:v", "1", "-vf", "scale=432:-2", os.path.splitext(OUT)[0] + "_capa.jpg")
    print("ok", OUT, f"{total:.1f}s", flush=True)

main()
