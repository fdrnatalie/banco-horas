"""Acha a janelinha da câmera (o rosto da Natalie) dentro da gravação de tela do app.

A interface do app é escura e de pouca cor; a câmera é uma foto colorida (parede vermelha, pele, luz).
Marca os pixels "de foto", fecha buracos e pega o maior bloco mais ou menos retangular.
"""
import numpy as np, cv2

def mask_foto(fr):
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)
    s, v = hsv[..., 1].astype(np.int16), hsv[..., 2].astype(np.int16)
    m = ((s > 70) & (v > 70)) | (v > 170)
    # a interface tem texto claro em linhas finas: a abertura remove isso, o fechamento une a foto
    m = m.astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    return m

def localizar(fr, ignorar_marca=True):
    """(x, y, w, h) da janela da câmera em coordenadas do quadro, ou None."""
    H, W = fr.shape[:2]
    m = mask_foto(cv2.resize(fr, (W // 2, H // 2), interpolation=cv2.INTER_AREA))
    if ignorar_marca: m[int(H / 2 * 0.88):, int(W / 2 * 0.86):] = 0       # selo "V RECORDER" no canto
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if w < 60 or h < 45: continue
        fill = a / float(w * h); ar = w / float(h)
        if fill < 0.55 or not (0.45 < ar < 2.2): continue
        if best is None or a > best[4]: best = (x, y, w, h, a)
    if best is None: return None
    x, y, w, h, _ = best
    return (2 * x, 2 * y, 2 * w, 2 * h)

def recorte(fr, box, w_out, h_out, inset=6):
    """recorta a janela (sem a borda) no formato w_out:h_out, centrado."""
    x, y, w, h = box
    y0 = max(y + inset, 44)                                   # nunca a barra de status do iPad
    c = fr[y0:y + h - inset, x + inset:x + w - inset]
    ch, cw = c.shape[:2]; asp = w_out / h_out
    if cw / ch > asp: nw = int(ch * asp); c = c[:, (cw - nw) // 2:(cw - nw) // 2 + nw]
    else: nh = int(cw / asp); c = c[(ch - nh) // 4:(ch - nh) // 4 + nh]
    return cv2.resize(c, (w_out, h_out), interpolation=cv2.INTER_AREA)

def valido(fr, box):
    """a caixa tem mesmo a câmera? (parede vermelha + pele; o app é escuro e quase sem cor)"""
    if not box: return False
    x, y, w, h = box
    if w < 150 or h < 150 or not (0.5 < w / h < 1.7): return False
    c = cv2.resize(fr[y:y + h, x:x + w], (max(1, w // 4), max(1, h // 4)), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV); H_, S, V = (hsv[..., i].astype(np.int16) for i in range(3))
    red = ((H_ < 8) | (H_ > 168)) & (S > 110) & (V > 60)
    skin = (H_ >= 5) & (H_ <= 22) & (S > 45) & (S < 170) & (V > 100)
    return (red.mean() + skin.mean()) > 0.2 and (V < 45).mean() < 0.4

def candidatos(grab, dur, n=48):
    """posições da janelinha ao longo do vídeo inteiro (ela muda de canto às vezes): lista de caixas completas."""
    det = []
    for t in np.linspace(5, max(6, dur - 5), n):
        f = grab(float(t)); b = localizar(f) if f is not None else None
        if b and valido(f, b): det.append(b)
    cl = []
    for b in det:
        for c in cl:
            if abs(c[0][0] - b[0]) < 60 and abs(c[0][1] - b[1]) < 60: c.append(b); break
        else: cl.append([b])
    out = []
    for c in cl:
        a = np.array(c, float)
        out.append((int(np.median(a[:, 0])), int(np.median(a[:, 1])), int(np.percentile(a[:, 2], 80)), int(np.percentile(a[:, 3], 80))))
    return out

def escolher(frames, cands=()):
    """caixa válida em pelo menos 3 de 4 amostras (detecção do trecho ou posição conhecida); senão None."""
    fs = [f for f in frames if f is not None]
    if not fs: return None
    opts = [b for b in (localizar(f) for f in fs) if b] + list(cands)
    best, bn = None, 0
    for b in opts:
        k = sum(valido(f, b) for f in fs)
        if k > bn or (k == bn and best and b[2] * b[3] > best[2] * best[3]): best, bn = b, k
    return tuple(int(v) for v in best) if best and bn >= max(1, len(fs) - 1) else None

def estavel(frames):
    """caixa só se TODAS as amostras acham a câmera no mesmo lugar; senão None (nada de app recortado)."""
    bs = [localizar(f) if f is not None else None for f in frames]
    if not bs or any(not valido(f, b) for f, b in zip(frames, bs)): return None
    a = np.array(bs, float)
    if (a[:, :2].max(0) - a[:, :2].min(0)).max() > 60: return None
    return tuple(int(v) for v in np.median(a, axis=0))

def mediana(boxes):
    bs = [b for b in boxes if b]
    if not bs: return None
    return tuple(int(v) for v in np.median(np.array(bs), axis=0))
