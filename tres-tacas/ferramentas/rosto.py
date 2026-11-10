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

def mediana(boxes):
    bs = [b for b in boxes if b]
    if not bs: return None
    return tuple(int(v) for v in np.median(np.array(bs), axis=0))
