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
X_L, X_R, Y_HEAD, Y_LIST, LH = 44, W - 44, 470, 590, 41
GREEN = (172, 200, 150)                              # verde sálvia (acerto), discreto
ROSE = (214, 140, 140)                               # rosé (erro)

def eventos():
    """lista de (t, estado) com estado = (esquerda[(nome, tipo)], direita[nome], novo, rodada)."""
    esq, dir_, out = [], [], []
    for e in P["rodada1"]:
        t, ok, nome = e[0], e[1] == "certo", e[2]
        (esq.append((nome, "1")) if ok else dir_.append(nome))
        out.append((t, (list(esq), list(dir_), ("L" if ok else "R", nome), 1)))
    for t, nome in P["rodada2"]:
        if nome == "*": moved = list(dir_); dir_.clear(); esq += [(n, "2") for n in moved]; novo = ("ALL", None)
        else: moved = ()
        if nome != "*":
            if nome in dir_: dir_.remove(nome)
            esq.append((nome, "2")); novo = ("L", nome)
        out.append((t, (list(esq), list(dir_), novo, 2, tuple(moved))))
    return out

def overlay(state, fade=1.0, hi=False, rodada_lbl=False):
    esq, dir_, novo, rod = state[:4] if state else ([], [], (None, None), 1)
    im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
    # faixas laterais translúcidas, só atrás das listas
    sh = np.zeros((H, W, 4), np.uint8)
    for x0, x1 in ((0, 340), (W - 340, W)):
        g = np.linspace(1, 0, x1 - x0) if x0 == 0 else np.linspace(0, 1, x1 - x0)
        a = (np.clip(g * 1.6, 0, 1) * 120).astype(np.uint8)
        yy = np.ones(H); yy[:Y_HEAD - 60] = 0; yy[Y_HEAD - 60:Y_HEAD] = np.linspace(0, 1, 60)
        yy[1400:] = 0; yy[1340:1400] = np.linspace(1, 0, 60)
        sh[:, x0:x1, 3] = (a[None, :] * yy[:, None]).astype(np.uint8); sh[:, x0:x1, :3] = (12, 6, 9)
    im.alpha_composite(Image.fromarray(sh))
    d.text((W // 2, 262), P["titulo"], font=V.font("corm600", 96), fill=V.CHAMPAGNE + (255,), anchor="mm")
    d.text((W // 2, 340), P.get("sub", ""), font=V.font("corm_it500", 46), fill=V.CREAM + (235,), anchor="mm")
    if rod == 2 or rodada_lbl:
        d.text((W // 2, 400), "refazendo os que errei", font=V.font("osw500", 24), fill=V.LINE + (230,), anchor="mm")
    nL, nR = len(esq), len(dir_)
    d.text((X_L, Y_HEAD), "ACERTOS", font=V.font("osw500", 24), fill=GREEN + (240,), anchor="lm")
    d.text((X_L, Y_HEAD + 52), str(nL), font=V.font("corm600", 66), fill=V.CHAMPAGNE + (255,), anchor="lm")
    d.text((X_R, Y_HEAD), "ERROS", font=V.font("osw500", 24), fill=ROSE + (240,), anchor="rm")
    d.text((X_R, Y_HEAD + 52), str(nR), font=V.font("corm600", 66), fill=V.CHAMPAGNE + (255,), anchor="rm")
    fL, fL2 = V.font("corm500", 36), V.font("corm_it500", 36)
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
        cor = V.CHAMPAGNE if k == "corm600" else (V.LINE if k == "osw500" else V.CREAM)
        y += int(prev * 0.75 + sz * 0.75) if prev else 0; prev = sz
        d.text((W // 2, y), txt, font=V.font(k, sz), fill=cor + (255,), anchor="mm")
    return np.array(V.shadowed(im, 12, 200))

def enc(path, dur, af="apad"):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-i", VID, "-map", "0:v", "-map", "1:a", "-t", f"{dur:.3f}", "-af", af, "-c:v", "libx264", "-preset", "medium",
                             "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", path], stdin=subprocess.PIPE)

def main():
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VID], capture_output=True, text=True).stdout)
    END = 3.2; fim1 = P["fim_rodada1"]
    ev = eventos(); r1 = [e for e in ev if e[1][3] == 1]
    s1 = r1[-1][1]; acertos1 = len(s1[0]); erros1 = len(s1[1])
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
    fecha(ig, last_ig, [("DE PRIMEIRA", "osw500", 30), (f"{acertos1} acertos", "corm600", 104), (f"{erros1} para treinar de novo", "corm_it500", 56)])
    fecha(full, last, [("NO FIM", "osw500", 30), (f"{acertos1 + erros1} de {acertos1 + erros1}", "corm600", 112), ("todos certos", "corm_it500", 60)])
    for nm in ("aromas_instagram", "aromas_completo"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "40", "-i", f"{OUTD}/{nm}.mp4", "-frames:v", "1", "-vf", "scale=432:-2", f"{OUTD}/{nm}_capa.jpg"], check=True)
    print("ok", acertos1, erros1, n / FPS, flush=True)

if __name__ == "__main__": main()
