"""Monta o episódio do YouTube a partir de um roteiro por temas.

uso:
  python3 montar_yt.py roteiro.json plano            -> limpa as falas, monta a linha do tempo, áudio e legendas (pasta de trabalho)
  python3 montar_yt.py roteiro.json video A B        -> renderiza as peças [A, B) da linha do tempo (permite dividir em partes)
  python3 montar_yt.py roteiro.json final            -> junta as partes + áudio em <saida>.mp4 e gera a prévia leve

roteiro.json: {"titulo", "serie", "video", "trans", "hesit", "saida", "fix": {}, "frases_fix": [[de, para]],
               "blocos": [{"id", "capitulo", "sub", "falas": [{"a", "b", "texto"}],
                           "telas": [{"tipo": "app|aula|placar|comparacao", "titulo", "linhas", "entra_fala", "sai_fala"}]}],
               "cta"}
Regras da série: a legenda e as notas nunca cobrem o rosto; fala a 1,1x; sem ééé, tosse ou pausa dentro das falas.
"""
import os, sys, json, subprocess, wave, math, re
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual as V, rosto, cleanfala

R = json.load(open(sys.argv[1])); MODE = sys.argv[2]
R["saida"] = os.path.abspath(R["saida"]); R["video"] = os.path.abspath(R["video"])
WD = os.path.splitext(R["saida"])[0] + "_trab"; os.makedirs(WD, exist_ok=True)
FPS, SPEED = 30, 1.1
W, H = V.W, V.H
SX0, SY0, SX1, SY1 = 0, 40, 1512, 1050                        # tira a barra de status do iPad
PH = 880; PW = int(PH * (SX1 - SX0) / (SY1 - SY0)); PX = (W - PW) // 2; PY = 36
CAP_Y = 1002; BANNER_S = 3.4; INTRO_HOLD = 3.0; END_S = 6.0

def sh(*a, **k): return subprocess.run(list(a), check=True, **k)

def grab(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", R["video"], "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE).stdout
    return np.frombuffer(raw, np.uint8)[:1512 * 1050 * 3].reshape(1050, 1512, 3) if len(raw) >= 1512 * 1050 * 3 else None

# ---------------------------------------------------------------- plano
def plano():
    wav48 = f"{WD}/fonte48.wav"
    if not os.path.exists(wav48): sh("ffmpeg", "-v", "error", "-y", "-i", R["video"], "-vn", "-ac", "1", "-ar", "48000", wav48)
    C = cleanfala.Cleaner(R["trans"], R["hesit"], wav48)
    pecas, limpeza = [], []
    for bi, b in enumerate(R["blocos"]):
        telas = sorted(enumerate(b.get("telas", [])), key=lambda kt: kt[1].get("entra_fala", 0) or 0)
        for fi, f in enumerate(b["falas"]):
            ti = None
            for k, t in telas:
                e = t.get("entra_fala", 0) or 0; s = t.get("sai_fala", len(b["falas"]) - 1)
                if s is None: s = len(b["falas"]) - 1
                if e <= fi <= s: ti = k
            sub, drop = C.clean(f["a"], f["b"])
            limpeza.append(dict(bloco=b["id"], fala=fi, texto=f["texto"], tirado=drop))
            for a, bb in sub: pecas.append(dict(bloco=bi, fala=fi, tela=ti, a=a, b=bb))
    # tempos de saída: cartela de abertura segura alguns segundos, o resto corre na fala
    t = 0.0
    for i, p in enumerate(pecas):
        p["o0"] = t; t += (p["b"] - p["a"]) / SPEED; p["o1"] = t
    total = t + END_S
    # rosto por peça (mediana de 3 quadros)
    last = None
    for p in pecas:
        bs = [rosto.localizar(fr) for fr in (grab(p["a"] + (p["b"] - p["a"]) * q) for q in (0.2, 0.5, 0.8)) if fr is not None]
        box = rosto.mediana(bs); p["rosto"] = list(box) if box else None
    json.dump(dict(pecas=pecas, total=total), open(f"{WD}/plano.json", "w"), ensure_ascii=False)
    json.dump(limpeza, open(f"{WD}/limpeza.json", "w"), ensure_ascii=False, indent=1)
    audio(pecas, total, wav48)
    legendas()
    capitulos(pecas)
    print(f"plano: {len(pecas)} peças, {total / 60:.2f} min", flush=True)

def audio(pecas, total, wav48):
    w = wave.open(wav48); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    out = []; f = int(0.012 * sr)
    for p in pecas:
        seg = x[int(p["a"] * sr):int(p["b"] * sr)].copy()
        lv = np.percentile(np.abs(seg), 97) if len(seg) else 0
        if lv > 1e-4: seg *= float(np.clip(0.30 / lv, 0.5, 8.0))
        if len(seg) > 2 * f: seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        out.append(seg)
    v = np.concatenate(out) if out else np.zeros(sr)
    tmp = f"{WD}/voz_1x.wav"; _wav(tmp, v, sr)
    chain = ("highpass=f=75,lowpass=f=14000,afftdn=nr=10:nf=-40,"
             "acompressor=threshold=0.08:ratio=3:attack=8:release=120:makeup=2,"
             f"loudnorm=I=-16:TP=-1.5:LRA=9,atempo={SPEED}")
    sh("ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", chain, "-ar", "48000", "-ac", "1", f"{WD}/voz.wav")
    w2 = wave.open(f"{WD}/voz.wav"); vv = np.frombuffer(w2.readframes(w2.getnframes()), np.int16).astype(np.float32) / 32768
    mix = np.zeros(int(total * 48000) + 48000, np.float32); mix[:len(vv)] += vv[:len(mix)]
    for p in pecas:                                     # um "pop" discreto quando entra uma tela nova
        pass
    _wav(f"{WD}/mix.wav", np.clip(mix[:int(total * 48000)], -1, 1), 48000)

def _wav(path, x, sr):
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def legendas():
    """transcreve a voz final (sempre de novo: transcrição velha desalinha a legenda) e corrige termos."""
    from faster_whisper import WhisperModel
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    w = wave.open(f"{WD}/voz.wav"); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    import scipy.signal as ss
    x16 = ss.resample_poly(x, 1, 3).astype(np.float32)
    segs, _ = m.transcribe(x16, language="pt", word_timestamps=True, vad_filter=False)
    words = [[ww.word.strip(), ww.start, ww.end] for s in segs for ww in s.words if ww.word.strip(".,!?…;: ")]
    merged = []                                         # "14" ",5" "%" -> "14,5%"
    for wd in words:
        if merged and (wd[0][:1] in ",.%" and (wd[0][1:2].isdigit() or wd[0] == "%")): merged[-1][0] += wd[0]; merged[-1][2] = wd[2]
        else: merged.append(wd)
    words = merged
    fix = {k.lower(): v for k, v in R.get("fix", {}).items()}
    for wd in words:
        core = wd[0].strip(".,!?…;:"); k = core.lower()
        if k in fix: wd[0] = wd[0].replace(core, fix[k])
    for a, b in R.get("frases_fix", []):
        aw = a.lower().split(); i = 0
        while i <= len(words) - len(aw):
            if [x_[0].lower().strip(".,!?…;:") for x_ in words[i:i + len(aw)]] == aw:
                bw = b.split(); t0, t1 = words[i][1], words[i + len(aw) - 1][2]; d = (t1 - t0) / len(bw)
                tail = re.search(r"[.,!?…]*$", words[i + len(aw) - 1][0]).group()
                new = [[bw[k], t0 + k * d, t0 + (k + 1) * d] for k in range(len(bw))]
                if not new[-1][0][-1:] in ".,!?…": new[-1][0] += tail
                words[i:i + len(aw)] = new; i += len(bw)
            else: i += 1
    lines, cur = [], []
    for wd in words:
        if cur and (len(cur) >= 6 or len(" ".join(x_[0] for x_ in cur + [wd])) > 40 or wd[1] - cur[-1][2] > 0.7):
            lines.append(cur); cur = []
        cur.append(wd)
        if wd[0][-1:] in ".?!": lines.append(cur); cur = []
    if cur: lines.append(cur)
    caps = []
    for k, ln in enumerate(lines):
        end = min(lines[k + 1][0][1] if k + 1 < len(lines) else ln[-1][2] + 0.6, ln[-1][2] + 0.8)
        caps.append(dict(a=ln[0][1], b=end, txt=[x_[0] for x_ in ln]))
    json.dump(caps, open(f"{WD}/legendas.json", "w"), ensure_ascii=False)
    def ts(x_): h = int(x_ // 3600); mm = int(x_ % 3600 // 60); s = x_ % 60; return f"{h:02d}:{mm:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
    with open(os.path.splitext(R["saida"])[0] + ".srt", "w") as f:
        for k, c in enumerate(caps, 1): f.write(f"{k}\n{ts(c['a'])} --> {ts(c['b'])}\n{' '.join(c['txt'])}\n\n")

def capitulos(pecas):
    seen, out = set(), []
    for p in pecas:
        if p["bloco"] in seen: continue
        seen.add(p["bloco"]); b = R["blocos"][p["bloco"]]; t = 0 if not out else p["o0"]
        out.append(f"{int(t // 60):02d}:{int(t % 60):02d} {b['capitulo']}")
    open(os.path.splitext(R["saida"])[0] + "_capitulos.txt", "w").write("\n".join(out) + "\n")

# ---------------------------------------------------------------- vídeo
def video(p_from, p_to):
    P = json.load(open(f"{WD}/plano.json")); pecas, total = P["pecas"], P["total"]
    caps = json.load(open(f"{WD}/legendas.json")); emph = set(R.get("destaques", []))
    capimg = [(c["a"], c["b"], V.caption(c["txt"], emph)) for c in caps]
    bg = V.background(R["serie"])
    banners = {bi: V.chapter_banner(bi, b["capitulo"], b.get("sub", "")) for bi, b in enumerate(R["blocos"])}
    cache = {}
    out = f"{WD}/parte_{p_from:04d}.mp4"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    first_of_block = {}
    for i, p in enumerate(pecas): first_of_block.setdefault(p["bloco"], p["o0"])
    fidx = int(round(pecas[p_from]["o0"] * FPS)); last_face = None
    for pi in range(p_from, p_to):
        p = pecas[pi]; fe = int(round(p["o1"] * FPS)); n = fe - fidx
        if n <= 0: continue
        cmd = ["ffmpeg", "-v", "error", "-ss", f"{p['a']:.3f}", "-t", f"{(p['b'] - p['a']) + 0.3:.3f}", "-i", R["video"],
               "-vf", f"setpts=(PTS-STARTPTS)/{SPEED},fps={FPS}", "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
        raw = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
        k_ = len(raw) // (1512 * 1050 * 3); frs = np.frombuffer(raw[:k_ * 1512 * 1050 * 3], np.uint8).reshape(k_, 1050, 1512, 3)
        if k_ == 0: frs = np.zeros((1, 1050, 1512, 3), np.uint8); k_ = 1
        if k_ < n: frs = np.concatenate([frs, np.repeat(frs[-1:], n - k_, 0)])
        b = R["blocos"][p["bloco"]]; tela = b["telas"][p["tela"]] if p["tela"] is not None else None
        box = tuple(p["rosto"]) if p["rosto"] else None
        if box: last_face = box
        key = (p["bloco"], p["tela"], box is not None and box[1] + box[3] / 2 > 525)
        if key not in cache: cache[key] = tela_layer(tela, box)
        layer = cache[key]
        for k in range(n):
            t = (fidx + k) / FPS; fr = bg.copy(); src = frs[k]
            compose(fr, src, tela, box, layer)
            dt = t - first_of_block[p["bloco"]]
            if p["bloco"] > 0 and 0 <= dt < BANNER_S and (tela is None or tela.get("tipo") == "app"):
                pr = min(1, dt / 0.4) if dt < BANNER_S - 0.4 else (BANNER_S - dt) / 0.4
                bn = banners[p["bloco"]].copy(); bn[..., 3] = (bn[..., 3] * pr).astype(np.uint8)
                V.over(fr, bn, PX + 40, PY + PH - 230)
            for ca, cb, img in capimg:
                if ca <= t < cb: V.over(fr, img, (W - img.shape[1]) // 2, CAP_Y - img.shape[0] // 2); break
            enc.stdin.write(fr.tobytes())
        fidx = fe
        if pi % 20 == 0: print(f"  peça {pi}/{len(pecas)} {fidx / FPS / 60:.2f} min", flush=True)
    if p_to >= len(pecas):
        endc = V.end_card(R["serie"], R.get("cta_tela", "o app que eu uso tá na descrição"))
        base = cv2.GaussianBlur(fr, (0, 0), 20)
        for k in range(int(round(total * FPS)) - fidx):
            pr = min(1, k / 15); f2 = (base.astype(np.float32) * (1 - 0.6 * pr)).astype(np.uint8)
            e = endc.copy(); e[..., 3] = (e[..., 3] * pr).astype(np.uint8); V.over(f2, e, 0, 0); enc.stdin.write(f2.tobytes())
    enc.stdin.close(); enc.wait(); print("ok", out, flush=True)

def tela_layer(tela, box):
    """parte fixa (cartões) de uma tela, pré-renderizada."""
    if tela is None: return None
    tipo = tela.get("tipo", "app"); tt = tela.get("titulo", ""); ll = tela.get("linhas", [])
    if tipo == "app":
        if not (tt or ll): return None
        return V.card(1100, tt, ll[:2], 46, 40)
    if tt.lower() == "capa": return V.cover(*(ll + ["", "", ""])[:3])
    if tipo in ("aula", "placar"): return V.card(1060 if box else 1500, tt, ll, 72, 50)
    if tipo == "comparacao":
        n = max(1, len(ll)); cw = ((1300 if box else 1740) - 30 * (n - 1)) // n
        cols = []
        for c in ll:
            parts = [x.strip() for x in re.split(r" · |;", c) if x.strip()]
            if len(parts) == 1 and ":" in parts[0]: h_, _, b_ = parts[0].partition(":"); parts = [h_, b_.strip()]
            cols.append(V.card(cw, parts[0], parts[1:], 42, 38))
        return dict(titulo=tt, cols=cols, cw=cw)
    return None

def face_tile(src, box, w, h):
    """rosto recortado; a janelinha pequena não é ampliada mais de 2x (fica nítida)."""
    W0, H0 = w, h
    if box[3] > box[2] * 1.1: w, h = int(h * 0.75), h          # janela vertical: recorte 3:4, rosto inteiro
    k = min(1.0, 2.0 * (box[2] - 12) / w, 2.0 * (box[3] - 12) / h); w2, h2 = int(w * k), int(h * k)
    return rosto.recorte(src, box, w2, h2), (W0 - w2) // 2, (H0 - h2) // 2

def compose(fr, src, tela, box, layer):
    tipo = tela.get("tipo", "app") if tela else "app"
    if tipo == "app" or layer is None and tipo != "aula":
        sc = cv2.resize(src[SY0:SY1, SX0:SX1], (PW, PH), interpolation=cv2.INTER_AREA)
        p, m = V.rounded(sc[..., ::-1], 24); V.over(fr, p, PX - m, PY - m)
        if layer is not None and isinstance(layer, np.ndarray):
            top = box is not None and box[1] + box[3] / 2 > 525           # nota vai na metade sem o rosto
            V.over(fr, layer, PX + 40, PY + 40 if (top or box is None) else PY + PH - 40 - layer.shape[0])
        return
    if tela.get("titulo", "").lower() == "capa":
        V.over(fr, layer, 0, 0)
        if box: f, dx, dy = face_tile(src, box, 560, 420); p, m = V.rounded(f[..., ::-1], 28); V.over(fr, p, 1260 - m + dx, 230 - m + dy)
        return
    if tipo in ("aula", "placar"):
        V.over(fr, layer, 90, max(70, (950 - layer.shape[0]) // 2))
        if box: f, dx, dy = face_tile(src, box, 640, 480); p, m = V.rounded(f[..., ::-1], 28); V.over(fr, p, 1200 - m + dx, 260 - m + dy)
        return
    if tipo == "comparacao":
        import PIL.Image as I, PIL.ImageDraw as D
        im = I.new("RGBA", (W, 130)); d = D.Draw(im)
        d.text((100, 65), layer["titulo"], font=V.font("corm600", 66), fill=V.CHAMPAGNE + (255,), anchor="lm")
        V.over(fr, np.array(im), 0, 50)
        for i, c in enumerate(layer["cols"]): V.over(fr, c, 90 + i * (layer["cw"] + 30), 190)
        if box: f, dx, dy = face_tile(src, box, 400, 300); p, m = V.rounded(f[..., ::-1], 24); V.over(fr, p, 1440 - m + dx, 600 - m + dy)

# ---------------------------------------------------------------- final
def final():
    partes = sorted(x for x in os.listdir(WD) if x.startswith("parte_"))
    with open(f"{WD}/lista.txt", "w") as f:
        for x in partes: f.write(f"file '{WD}/{x}'\n")
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/lista.txt", "-i", f"{WD}/mix.wav",
       "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", R["saida"])
    # prévia leve para o painel (cabe no limite de 20 MB)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", R["saida"]],
                               stdout=subprocess.PIPE, text=True).stdout)
    vk = max(150, int((19 * 8 * 1024) / dur) - 64)
    prev = os.path.splitext(R["saida"])[0] + "_previa.mp4"
    sh("ffmpeg", "-v", "error", "-y", "-i", R["saida"], "-vf", "scale=854:-2", "-c:v", "libx264", "-preset", "slow", "-b:v", f"{vk}k",
       "-maxrate", f"{int(vk * 1.3)}k", "-bufsize", f"{vk * 2}k", "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-movflags", "+faststart", prev)
    print("final:", R["saida"], prev, f"{dur / 60:.2f} min", flush=True)

if MODE == "plano": plano()
elif MODE == "video": video(int(sys.argv[3]), int(sys.argv[4]))
elif MODE == "final": final()
