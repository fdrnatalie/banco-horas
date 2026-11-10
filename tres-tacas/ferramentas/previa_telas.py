"""Prévia de cada tela de um roteiro, com o mesmo visual do vídeo final (para aprovação no painel).

uso: python3 previa_telas.py roteiro.json pasta_saida
Gera <bloco>_<tela>.jpg (1280x720) e indice.json com as telas e as falas de cada uma.
"""
import os, sys, json
roteiro, outdir = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], roteiro, "nenhum"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2
import montar_yt as M, visual as V, rosto

os.makedirs(outdir, exist_ok=True)
bg = V.background(M.R["serie"]); idx = []
for bi, b in enumerate(M.R["blocos"]):
    telas = sorted(enumerate(b.get("telas", [])), key=lambda kt: kt[1].get("entra_fala", 0) or 0)
    if not telas: telas = [(None, None)]
    for k, t in telas:
        e = (t or {}).get("entra_fala", 0) or 0
        s = (t or {}).get("sai_fala", len(b["falas"]) - 1)
        if s is None: s = len(b["falas"]) - 1
        falas = b["falas"][e:s + 1] if b["falas"] else []
        f0 = falas[0] if falas else (b["falas"][-1] if b["falas"] else None)
        tt = (f0["a"] + min(1.2, (f0["b"] - f0["a"]) / 2)) if f0 else 0
        src = M.grab(tt)
        if src is None: src = np.zeros((1050, 1512, 3), np.uint8)
        box = rosto.localizar(src)
        fr = bg.copy(); M.compose(fr, src, t, box, M.tela_layer(t, box))
        if f0:
            ws = f0["texto"].split(); cap = V.caption(ws[:7] + (["…"] if len(ws) > 7 else []))
            V.over(fr, cap, (V.W - cap.shape[1]) // 2, M.CAP_Y - cap.shape[0] // 2)
        name = f"{b['id']}_{k if k is not None else 0}.jpg"
        cv2.imwrite(os.path.join(outdir, name), cv2.resize(fr, (1280, 720), interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 84])
        idx.append(dict(bloco=b["id"], capitulo=b.get("capitulo", ""), sub=b.get("sub", ""), tema=b.get("tema", ""),
                        tipo=(t or {}).get("tipo", "app"), titulo=(t or {}).get("titulo", ""), linhas=(t or {}).get("linhas", []),
                        fonte=(t or {}).get("fonte", ""), img=name, falas=[f["texto"] for f in falas]))
        print(name, flush=True)
json.dump(idx, open(os.path.join(outdir, "indice.json"), "w"), ensure_ascii=False, indent=1)
