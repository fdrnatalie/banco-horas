"""Teste de aromas às cegas: título + placar (acertos à esquerda, erros à direita) por cima do vídeo já editado.

uso: python3 aromas_placar.py placar.json pasta_saida
Gera: aromas_instagram.mp4 (só até acabarem os potinhos, com cartão final) e aromas_completo.mp4 (com a rodada dos errados).
Nada é desenhado no meio da tela (rosto) nem na faixa das legendas que já vêm no vídeo.
"""
import os, sys, json, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import visual as V

P = json.load(open(sys.argv[1])); OUTD = sys.argv[2]; os.makedirs(OUTD, exist_ok=True)
VID = P["video"]; W, H, FPS = 1080, 1920, 30
FADE = 6; HI = 1.4                                   # quadros de entrada; segundos em destaque
X_L, X_R, Y_HEAD, Y_LIST, LH = 130, W - 130, 470, 590, 40   # longe das bordas: o Reels corta ~100 px de cada lado
F_TIT, F_TIT_IT, F_LBL, F_ITEM, F_ITEM2 = "dmserif", "dmserif_it", "jost500", "jost400", "jost300"
GREEN = (172, 200, 150)                              # verde sálvia (acerto), discreto
ROSE = (214, 140, 140)                               # rosé (erro)

def eventos():
    """lista de (t, estado) com estado = (esquerda[(nome, tipo)], direita[nome], novo, rodada)."""
    esq, dir_, out = [], [], []
    for e in P["rodada1"]:
        t, ok, nome = e[0], e[1] == "certo", e[2]
        (esq.append((nome, "1")) if ok else dir_.append(nome))
        out.append((t, (list(esq), list(dir_), ("L" if ok else "R", nome), 1)))
    for t, nome, *resto in P["rodada2"]:
        if nome == "*":                              # fim: passa tudo para a esquerda, menos os que ficaram sem acertar
            fica = resto[0] if resto else []
            moved = [n for n in dir_ if n not in fica]; dir_[:] = [n for n in dir_ if n in fica]
            esq += [(n, "2") for n in moved]; novo = ("ALL", None)
        else: moved = ()
        if nome != "*":
            if nome in dir_: dir_.remove(nome)
            esq.append((nome, "2")); novo = ("L", nome)
        out.append((t, (list(esq), list(dir_), novo, 2, tuple(moved))))
    return out

def spaced(d, x, y, txt, font, fill, anchor="lm", track=3):
    """texto com espaçamento entre letras (rótulos em caixa alta)."""
    w = sum(font.getlength(c) for c in txt) + track * (len(txt) - 1)
    x0 = x - w if anchor[0] == "r" else (x - w / 2 if anchor[0] == "m" else x)
    for c in txt: d.text((x0, y), c, font=font, fill=fill, anchor="l" + anchor[1]); x0 += font.getlength(c) + track

def overlay(state, fade=1.0, hi=False, rodada_lbl=False):
    esq, dir_, novo, rod = state[:4] if state else ([], [], (None, None), 1)
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    # faixas laterais translúcidas, só atrás das listas
    sh = np.zeros((H, W, 4), np.uint8)
    for x0, x1 in ((0, 480), (W - 480, W)):
        g = np.linspace(1, 0, x1 - x0) if x0 == 0 else np.linspace(0, 1, x1 - x0)
        a = (np.clip(g * 1.5, 0, 1) * 105).astype(np.uint8)
        yy = np.ones(H); yy[:Y_HEAD - 60] = 0; yy[Y_HEAD - 60:Y_HEAD] = np.linspace(0, 1, 60)
        yy[1400:] = 0; yy[1340:1400] = np.linspace(1, 0, 60)
        sh[:, x0:x1, 3] = (a[None, :] * yy[:, None]).astype(np.uint8); sh[:, x0:x1, :3] = (12, 6, 9)
    im.alpha_composite(Image.fromarray(sh))
    d.text((W // 2, 262), P["titulo"], font=V.font(F_TIT, 92), fill=V.CHAMPAGNE + (255,), anchor="mm")
    d.text((W // 2, 338), P.get("sub", ""), font=V.font(F_TIT_IT, 44), fill=V.CREAM + (235,), anchor="mm")
    if rod == 2 or rodada_lbl:
        spaced(d, W // 2, 398, "REFAZENDO OS QUE ERREI", V.font(F_LBL, 21), V.LINE + (235,), "mm", 3)
    nL, nR = len(esq), len(dir_)
    spaced(d, X_L, Y_HEAD, "ACERTOS", V.font(F_LBL, 22), GREEN + (245,), "lm", 4)
    d.text((X_L, Y_HEAD + 54), str(nL), font=V.font(F_TIT, 64), fill=V.CHAMPAGNE + (255,), anchor="lm")
    spaced(d, X_R, Y_HEAD, "ERROS", V.font(F_LBL, 22), ROSE + (245,), "rm", 4)
    d.text((X_R, Y_HEAD + 54), str(nR), font=V.font(F_TIT, 64), fill=V.CHAMPAGNE + (255,), anchor="rm")
    fL, fL2 = V.font(F_ITEM, 32), V.font(F_ITEM2, 32)
    def item(x, y, nome, anchor, f, cor, is_new):
        a = int(255 * (fade if is_new else 1)); c = (V.CHAMPAGNE if (is_new and hi) else cor)
        dx = int((1 - fade) * 24) * (1 if anchor == "lm" else -1) if is_new else 0
        d.text((x - dx, y), nome, font=f, fill=c + (a,), anchor=anchor)
    if rod == 2:                                     # 2ª rodada: os de primeira viram uma linha só
        n1 = sum(1 for _, r in esq if r == "1")
        esq_v = [(f"{n1} de primeira", "x")] + [(nm, r) for nm, r in esq if r == "2"]
    else: esq_v = esq
    nLv = len(esq_v); moved_all = state[4] if state and len(state) > 4 else ()
    maxn = max(nLv, nR, 1); lh = LH if maxn <= 19 else int(LH * 19 / maxn)
    for k, (nome, r) in enumerate(esq_v):
        is_new = (novo[0] == "L" and nome == novo[1] and k == nLv - 1) or (novo[0] == "ALL" and r == "2" and nome in moved_all)
        item(X_L, Y_LIST + k * lh + (14 if r == "2" else 0), nome, "lm", fL2 if r == "2" else fL, GREEN if r == "x" else V.CREAM, is_new)
    for k, nome in enumerate(dir_):
        is_new = novo[0] == "R" and nome == novo[1] and k == nR - 1
        item(X_R, Y_LIST + k * lh, nome, "rm", fL, (205, 190, 180), is_new)
    return np.array(V.shadowed(im, 6, 200))

def cartao_final(linhas):
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im); y = 760; prev = 0
    for txt, k, sz in linhas:
        cor = V.CHAMPAGNE if k == F_TIT else (V.LINE if k == F_LBL else V.CREAM)
        y += int(prev * 0.75 + sz * 0.75) if prev else 0; prev = sz
        if k == F_LBL: spaced(d, W // 2, y, txt, V.font(k, sz), cor + (255,), "mm", 5)
        else: d.text((W // 2, y), txt, font=V.font(k, sz), fill=cor + (255,), anchor="mm")
    return np.array(V.shadowed(im, 12, 200))

def sfx(ev, total, path, sr=48000):
    """sons baixinhos: 'tim' de vidro no acerto, dois toques graves e suaves no erro."""
    y = np.zeros(int((total + 2) * sr), np.float32)
    def tom(f, dur, amp, decay):
        t = np.arange(int(dur * sr)) / sr; env = np.exp(-t / decay) * np.minimum(1, t / 0.004)
        return (amp * env * np.sin(2 * np.pi * f * t)).astype(np.float32)
    certo = tom(1568, 0.7, 0.040, 0.16) + tom(2093, 0.7, 0.028, 0.12) + tom(3136, 0.7, 0.008, 0.06)
    e1, e2 = tom(311, 0.22, 0.060, 0.07) + tom(622, 0.22, 0.012, 0.04), tom(247, 0.3, 0.060, 0.09) + tom(494, 0.3, 0.012, 0.05)
    errado = np.zeros(int(0.5 * sr), np.float32); errado[:len(e1)] += e1; errado[int(0.13 * sr):int(0.13 * sr) + len(e2)] += e2
    def put(t, s):
        i = int(t * sr); m = max(0, min(len(s), len(y) - i)); y[i:i + m] += s[:m]
    for t, st in ev:
        kind = st[2][0]
        if kind == "R": put(t, errado)
        elif kind == "ALL":
            for k in range(3): put(t + 0.11 * k, certo * (0.9 + 0.1 * k))
        else: put(t, certo)
    import wave
    w = wave.open(path, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def enc(path, dur, af="apad"):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-i", VID, "-i", f"{OUTD}/sons.wav", "-filter_complex", f"[1:a]{af}[v];[2:a]aresample=48000[s];[v][s]amix=inputs=2:normalize=0:duration=longest[a]",
                             "-map", "0:v", "-map", "[a]", "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium",
                             "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", path], stdin=subprocess.PIPE)

def main():
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VID], capture_output=True, text=True).stdout)
    END = 2.2; fim1 = P["fim_rodada1"]
    ev = eventos(); r1 = [e for e in ev if e[1][3] == 1]
    s1 = r1[-1][1]; acertos1 = len(s1[0]); erros1 = len(s1[1])
    sfx(ev, dur + END, f"{OUTD}/sons.wav")
    ig = enc(f"{OUTD}/aromas_instagram.mp4", fim1 + END, f"afade=t=out:st={fim1 - 0.3:.2f}:d=0.3,apad"); full = enc(f"{OUTD}/aromas_completo.mp4", dur + END)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", VID, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    cache = {}; n = 0; last_ig = last = None; fs = W * H * 3
    while True:
        raw = dec.stdout.read(fs)
        if len(raw) < fs: break
        t = n / FPS; fr = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy()
        i = max([k for k, e in enumerate(ev) if e[0] <= t], default=-1)
        if i < 0: key = ("none",); state = None; fade = 1; hi = False
        else:
            te, state = ev[i]; age = t - te; fstep = min(FADE, int(age * FPS))
            fade = fstep / FADE if fstep < FADE else 1.0; hi = age < HI; key = (i, fstep if fade < 1 else "f", hi)
        lbl = t >= fim1
        key = key + (lbl,)
        if key not in cache:
            if len(cache) > 40: cache.clear()
            cache[key] = overlay(state, fade, hi, lbl)
        V.over(fr, cache[key], 0, 0)
        if t < fim1: ig.stdin.write(fr.tobytes()); last_ig = fr
        full.stdin.write(fr.tobytes()); last = fr; n += 1
    dec.wait()
    def fecha(e, base, linhas):
        card = cartao_final(linhas); b = cv2.GaussianBlur(base, (0, 0), 20)
        for k in range(int(END * FPS)):
            pr = min(1, k / 10); f2 = (b.astype(np.float32) * (1 - 0.6 * pr)).astype(np.uint8)
            c = card.copy(); c[..., 3] = (c[..., 3] * pr).astype(np.uint8); V.over(f2, c, 0, 0); e.stdin.write(f2.tobytes())
        e.stdin.close(); e.wait()
    fecha(ig, last_ig, [("DE PRIMEIRA", F_LBL, 28), (f"{acertos1} acertos", F_TIT, 104), (f"{erros1} para treinar de novo", F_TIT_IT, 52)])
    fecha(full, last, [tuple(x) for x in P["fim_completo"]] if P.get("fim_completo") else
          [("NO FIM", F_LBL, 28), (f"{acertos1 + erros1} de {acertos1 + erros1}", F_TIT, 108), ("todos certos", F_TIT_IT, 56)])
    for nm in ("aromas_instagram", "aromas_completo"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "40", "-i", f"{OUTD}/{nm}.mp4", "-frames:v", "1", "-vf", "scale=432:-2", f"{OUTD}/{nm}_capa.jpg"], check=True)
    print("ok", acertos1, erros1, n / FPS, flush=True)

if __name__ == "__main__": main()
