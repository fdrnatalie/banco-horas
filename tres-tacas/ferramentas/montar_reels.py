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
R["frases_fix"] = R.get("frases_fix", []) + SP.get("frases_fix", []); R.setdefault("fix", {}).update(SP.get("fix", {}))
OUT = os.path.abspath(SP["saida"]); WD = os.path.splitext(OUT)[0] + "_trab"; os.makedirs(WD, exist_ok=True)
VID = os.path.abspath(R["video"]); FPS, SPEED = 30, 1.1
W, H = 1080, 1920
# tudo dentro da faixa 3:4 central (y 240-1680), que é o que aparece no grid do perfil; base livre para a interface do IG
LAY = {  # (cartão: x, y, w, h) , (rosto: x, y, w, h) , y da legenda
    "cartao+rosto": ((60, 540, 960, 380), (120, 1050, 840, 600), 985),
    "rosto": (None, (60, 560, 960, 720), 1390),
    "cartao": ((60, 600, 960, 560), None, 1300),
}
END_S = 2.5

def sh(*a): subprocess.run(list(a), check=True)

def grab(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", VID, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE).stdout
    return np.frombuffer(raw, np.uint8)[:1512 * 1050 * 3].reshape(1050, 1512, 3) if len(raw) >= 1512 * 1050 * 3 else None

def background():
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W * 0.5) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
    c1, c2 = np.array([0x22, 0x14, 0x2c], np.float32), np.array([0x0e, 0x06, 0x12], np.float32)
    t = np.clip(d * 1.3, 0, 1)[..., None]; bg = c1 * (1 - t) + c2 * t
    bg += np.random.default_rng(7).normal(0, 2.2, bg.shape[:2])[..., None]
    return np.clip(bg, 0, 255).astype(np.uint8)

def header():
    im = Image.new("RGBA", (W, 540)); d = ImageDraw.Draw(im)
    d.text((W // 2, 300), R["serie"].upper(), font=V.font("osw500", 26), fill=V.LINE + (230,), anchor="mm")
    d.line([(W // 2 - 40, 326), (W // 2 + 40, 326)], fill=V.LINE + (150,), width=1)
    ws = SP["gancho"].split()
    for sz in (76, 70, 64, 58):                          # o título nunca sai cortado: diminui até caber
        f = V.font("corm600", sz)
        if f.getlength(SP["gancho"]) <= W - 200: lines = [SP["gancho"]]
        else:                                            # duas linhas equilibradas, sem palavra sozinha
            k = min(range(1, len(ws)), key=lambda i: max(f.getlength(" ".join(ws[:i])), f.getlength(" ".join(ws[i:]))))
            lines = [" ".join(ws[:k]), " ".join(ws[k:])]
        if max(f.getlength(l) for l in lines) <= W - 200: break
    y = 410 if len(lines) == 1 else 385
    for ln in lines: d.text((W // 2, y), ln, font=f, fill=V.CHAMPAGNE + (255,), anchor="mm"); y += int(sz * 1.08)
    return np.array(V.shadowed(im, 12, 170))

def wrap(txt, f, maxw):
    out, cur = [], ""
    for w in txt.split():
        if cur and f.getlength(cur + " " + w) > maxw: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: out.append(cur)
    return out

def ctx_layer(tela, w=960, hmax=None):
    if tela is None or tela.get("tipo") == "app" and not (tela.get("titulo") or tela.get("linhas")): return None
    tipo = tela.get("tipo"); tt = tela.get("titulo", ""); ll = tela.get("linhas", [])
    if tt.lower() == "capa": return None
    if tipo == "comparacao":
        ll = [" · ".join(x.strip() for x in re.split(r" · |;", c)) for c in ll]
    for ts, ls in ((64, 52), (58, 46), (54, 42), (50, 38), (46, 34)):   # o cartão nunca invade a legenda
        c = V.card(w, tt, ll[:4], ts, ls)
        if hmax is None or c.shape[0] <= hmax: break
    return c

def pecas():
    blocos = {b["id"]: b for b in R["blocos"]}
    wav48 = f"{WD}/fonte48.wav"
    if not os.path.exists(wav48): sh("ffmpeg", "-v", "error", "-y", "-i", VID, "-vn", "-ac", "1", "-ar", "48000", wav48)
    C = cleanfala.Cleaner(R["trans"], R["hesit"], wav48)
    out = []
    for item in SP["blocos"]:
        bid, sel = (item, None) if isinstance(item, str) else (item["bloco"], item.get("falas"))
        b = blocos[bid]; telas = SP.get("telas", {}).get(bid, b.get("telas", []))
        for fi, f in enumerate(b["falas"]):
            if sel is not None and fi not in sel: continue
            tela = None
            for t in telas:
                e = t.get("entra_fala", 0) or 0; s = t.get("sai_fala", len(b["falas"]) - 1)
                if s is None: s = len(b["falas"]) - 1
                if e <= fi <= s: tela = t
            if SP.get("continuo", True): continue
            sub, _ = C.clean(f["a"], f["b"])
            for a, bb in sub: out.append(dict(a=a, b=bb, tela=tela, cap=b))
        if SP.get("continuo", True) and b["falas"]:
            # falas próximas no bruto viram um trecho só (nada do meio se perde); saem só pausas longas, ééé e tosse
            fs = [(fi, f) for fi, f in enumerate(b["falas"]) if sel is None or fi in sel]
            runs = []
            for fi, f in fs:
                if runs and 0 <= f["a"] - runs[-1][1] < 4.0: runs[-1][1] = max(runs[-1][1], f["b"]); runs[-1][2].append(fi)
                else: runs.append([f["a"], f["b"], [fi]])
            for a0, b0, fis in runs:
              sub, _ = C.clean(a0, b0, gap=0.6, pad=0.12, tail=0.2)
              for a, bb in sub:
                tela = None
                for t in telas:
                    e = t.get("entra_fala", 0) or 0; s_ = t.get("sai_fala", len(b["falas"]) - 1)
                    if s_ is None: s_ = len(b["falas"]) - 1
                    if any(e <= fi <= s_ for fi in fis): tela = t
                out.append(dict(a=a, b=bb, tela=tela, cap=b))
    if SP.get("fecho"):                                  # fala de finalização ("Bom, é isso.")
        sub, _ = C.clean(*SP["fecho"], gap=0.6, pad=0.12, tail=0.35)
        for a, bb in sub: out.append(dict(a=a, b=bb, tela=None, cap=None))
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
    merged = []                                         # "14" ",5" "%" -> "14,5%"
    for wd in words:
        if merged and (wd[0][:1] in ",.%" and (wd[0][1:2].isdigit() or wd[0] == "%")): merged[-1][0] += wd[0]; merged[-1][2] = wd[2]
        else: merged.append(wd)
    words = merged
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
    capimg = [(a, b, V.caption(t, emph, size=54, maxw=980)) for a, b, t in caps]
    bg = background(); hd = header(); cache = {}
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", f"{WD}/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    CAM = SP.get("camadas")                              # pacote para o CapCut: vídeo base sem texto + PNGs + .srt + tempos
    if CAM:
        PK = os.path.splitext(OUT)[0] + "_capcut"; os.makedirs(PK, exist_ok=True)
        enc2 = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                 "-i", f"{WD}/mix.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                                 "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", f"{PK}/1_video_base.mp4"], stdin=subprocess.PIPE)
        segs_cart = []
    fidx = 0; last = None; box = None
    cf = f"{WD}/janelas.json"
    if os.path.exists(cf): CANDS = [tuple(c) for c in json.load(open(cf))]
    else:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VID], capture_output=True, text=True).stdout)
        CANDS = rosto.candidatos(grab, dur); json.dump(CANDS, open(cf, "w"))
    print("janelas", CANDS, flush=True)
    for p in ps:
        fe = int(round(p["o1"] * FPS)); n = fe - fidx
        if n <= 0: continue
        box = rosto.escolher([grab(p["a"] + (p["b"] - p["a"]) * q) for q in (0.1, 0.4, 0.7, 0.95)], CANDS)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{p['a']:.3f}", "-t", f"{p['b'] - p['a'] + 0.3:.3f}", "-i", VID,
                              "-vf", f"setpts=(PTS-STARTPTS)/{SPEED},fps={FPS}", "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                             stdout=subprocess.PIPE).stdout
        k_ = len(raw) // (1512 * 1050 * 3); frs = np.frombuffer(raw[:k_ * 1512 * 1050 * 3], np.uint8).reshape(k_, 1050, 1512, 3)
        if k_ == 0: frs = np.zeros((1, 1050, 1512, 3), np.uint8); k_ = 1
        if k_ < n: frs = np.concatenate([frs, np.repeat(frs[-1:], n - k_, 0)])
        tela = p["tela"]
        if tela is None and box is None and p.get("cap"):     # sem rosto e sem cartão: cartão do capítulo (nunca o app)
            tela = {"tipo": "aula", "titulo": p["cap"].get("capitulo", ""), "linhas": [p["cap"]["sub"]] if p["cap"].get("sub") else []}
        if tela is None and box is None: tela = {"tipo": "aula", "titulo": R["serie"], "linhas": []}
        lay = ("cartao+rosto" if box else "cartao") if ctx_layer(tela) is not None else "rosto"
        CTX, FACE, CAP_Y = LAY[lay]
        key = (json.dumps(tela, sort_keys=True), lay)
        if key not in cache: cache[key] = ctx_layer(tela, CTX[2], CTX[3] + 30) if CTX else None
        layer = cache[key]
        if CAM and layer is not None:
            if segs_cart and segs_cart[-1][0] == key and abs(segs_cart[-1][2] - fidx / FPS) < 0.05: segs_cart[-1][2] = fe / FPS
            else: segs_cart.append([key, fidx / FPS, fe / FPS, layer, CTX])
        for k in range(n):
            t = (fidx + k) / FPS; fr = bg.copy(); src = frs[k]
            if box and FACE:
                fw, fh = FACE[2], FACE[3]
                if box[3] > box[2] * 1.1: fw = int(fh * 0.75)
                kk = min(1.0, 2.2 * (box[2] - 12) / fw, 2.2 * (box[3] - 12) / fh); fw2, fh2 = int(fw * kk), int(fh * kk)
                face = rosto.recorte(src, box, fw2, fh2); pp, m = V.rounded(face[..., ::-1], 30)
                V.over(fr, pp, FACE[0] + (FACE[2] - fw2) // 2 - m, FACE[1] + (FACE[3] - fh2) // 2 - m)
            if CAM: enc2.stdin.write(fr.tobytes()); last_base = fr.copy()
            V.over(fr, hd, 0, 0)
            if layer is not None: V.over(fr, layer, CTX[0], CTX[1] + max(0, (CTX[3] - layer.shape[0]) // 2))
            for ca, cb, img in capimg:
                if ca <= t < cb: V.over(fr, img, (W - img.shape[1]) // 2, CAP_Y - img.shape[0] // 2); break
            enc.stdin.write(fr.tobytes()); last = fr

        fidx = fe
    endimg = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(endimg)
    d.text((W // 2, 800), "a degustação completa", font=V.font("corm_it500", 64), fill=V.CREAM + (240,), anchor="mm")
    d.text((W // 2, 910), SP.get("fim", "no YouTube"), font=V.font("corm600", 104), fill=V.CHAMPAGNE + (255,), anchor="mm")
    d.text((W // 2, 1010), "LINK NA BIO", font=V.font("osw500", 30), fill=V.LINE + (230,), anchor="mm")
    endimg = np.array(V.shadowed(endimg, 12, 200)); base = cv2.GaussianBlur(last, (0, 0), 18)
    if CAM: base2 = cv2.GaussianBlur(last_base, (0, 0), 18)
    for k in range(int(round(total * FPS)) - fidx):
        pr = min(1, k / 10); f2 = (base.astype(np.float32) * (1 - 0.55 * pr)).astype(np.uint8)
        if CAM: enc2.stdin.write((base2.astype(np.float32) * (1 - 0.55 * pr)).astype(np.uint8).tobytes())
        e = endimg.copy(); e[..., 3] = (e[..., 3] * pr).astype(np.uint8); V.over(f2, e, 0, 0); enc.stdin.write(f2.tobytes())
    enc.stdin.close(); enc.wait()
    if CAM: enc2.stdin.close(); enc2.wait(); camadas(PK, hd, segs_cart, caps, endimg, fidx / FPS, total)
    sh("ffmpeg", "-v", "error", "-y", "-ss", "1.5", "-i", OUT, "-frames:v", "1", "-vf", "scale=432:-2", os.path.splitext(OUT)[0] + "_capa.jpg")
    print("ok", OUT, f"{total:.1f}s", flush=True)

def tc(t, srt=True):
    h, r = divmod(t, 3600); m, s_ = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s_):02d},{int(round((s_ % 1) * 1000)) % 1000:03d}" if srt else f"{int(m)}:{s_:04.1f}"

def camadas(PK, hd, segs, caps, endimg, t_fim, total):
    def full(rgba, x, y):
        im = np.zeros((H, W, 4), np.uint8); h_, w_ = rgba.shape[:2]
        im[y:y + h_, x:x + w_] = rgba[:H - y, :W - x]; return im
    Image.fromarray(full(hd, 0, 0)).save(f"{PK}/2_titulo.png")
    lst = [f"VÍDEO BASE: 1_video_base.mp4 ({tc(total, False)}). Já tem a sua voz limpa, o fundo e o seu rosto no lugar; nada de texto.",
           "Cada PNG é do tamanho da tela inteira (1080x1920), com o elemento já na posição certa: é só colocar como sobreposição,",
           "esticar até ocupar a tela toda e ajustar o começo e o fim pelos tempos abaixo.", "",
           f"2_titulo.png ............ 0:00.0 até {tc(t_fim, False)} (o vídeo todo, menos o final)"]
    for i, (key, a, b, layer, CTX) in enumerate(segs, 3):
        nm = f"{i}_cartao.png"; Image.fromarray(full(layer, CTX[0], CTX[1] + max(0, (CTX[3] - layer.shape[0]) // 2))).save(f"{PK}/{nm}")
        lst.append(f"{nm:<24}{tc(a, False)} até {tc(b, False)}  ({json.loads(key[0]).get('titulo', '')})")
    nm = f"{len(segs) + 3}_final.png"; Image.fromarray(endimg).save(f"{PK}/{nm}")
    lst.append(f"{nm:<24}{tc(t_fim, False)} até o fim (entra com um esmaecer curto)")
    with open(f"{PK}/legendas.srt", "w") as f:
        for k, (a, b, t) in enumerate(caps, 1): f.write(f"{k}\n{tc(a)} --> {tc(b)}\n{' '.join(t)}\n\n")
    lst += ["", "LEGENDAS: legendas.srt (já revisadas). No CapCut do iPad o caminho mais rápido é Texto > Legendas automáticas (português)",
            "e conferir com o .srt; no CapCut do computador dá para importar o .srt direto.",
            "Posição da legenda que eu uso: entre o cartão e o rosto (nunca em cima do rosto), fonte Inter, creme."]
    open(f"{PK}/0_LEIA_tempos.txt", "w").write("\n".join(lst) + "\n")
    sh("bash", "-c", f"cd '{os.path.dirname(PK)}' && rm -f '{PK}.zip' && zip -qr '{PK}.zip' '{os.path.basename(PK)}'")
    print("pacote", PK + ".zip", flush=True)

main()
