"""Acerta o momento de cada nome no placar: transcreve de novo uma janela curta em volta do tempo aproximado
(tempo por palavra, sem VAD) e usa o fim da palavra que bate com o nome. Assim o nome entra quando ela fala.

uso: python3 aromas_refinar.py placar.json video_original [janela_antes=8] [janela_depois=4]
Grava por cima do placar.json (guarda o tempo antigo em placar.json.bak) e imprime o que mudou.
"""
import sys, json, subprocess, unicodedata, shutil
import numpy as np
from faster_whisper import WhisperModel

PJ, VID = sys.argv[1], sys.argv[2]
A = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0; B = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
P = json.load(open(PJ)); shutil.copy(PJ, PJ + ".bak")
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VID, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 stdout=subprocess.PIPE, check=True).stdout, np.float32)
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
norm = lambda s: "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn" and c.isalpha())
APELIDO = {"guaiaba": "goiaba", "papaya": "", "jasmin": "jasmim", "pimentao": "pimentao"}

def acha(nome, t0):
    a = max(0, t0 - A); b = t0 + B
    seg = x[int(a * 16000):int(b * 16000)]
    segs, _ = m.transcribe(seg, language="pt", word_timestamps=True, vad_filter=False, condition_on_previous_text=False,
                           initial_prompt=f"{nome}.")
    words = [(a + w.start, a + w.end, norm(w.word)) for s in segs for w in s.words]
    alvo = norm(nome.split()[0])[:5]; best = None
    for i, (s, e, w) in enumerate(words):
        w = APELIDO.get(w, w)
        if w.startswith(alvo[:4]) or (len(alvo) >= 4 and alvo[:4] in w):
            fim = e
            for s2, e2, w2 in words[i + 1:i + 3]:      # nomes compostos: "casca de laranja", "doce de leite"
                if norm(nome).startswith(norm(nome.split()[0]) + w2[:2]) or w2 in norm(nome): fim = e2
            if best is None or abs(fim - t0) < abs(best - t0): best = fim
    return best

for e in P["rodada1"]:
    t0, nome = e[0], e[2]
    t = acha(nome, t0)
    if t is not None and abs(t - t0) > 0.3: print(f"{nome:<18} {t0:8.1f} -> {t:8.1f}"); e[0] = round(t + 0.1, 2)
    elif t is None: print(f"{nome:<18} {t0:8.1f}  (não achei a palavra; mantido)")
P["rodada1"].sort(key=lambda e: e[0])
for e in P.get("rodada2", []):
    if e[1] == "*": continue
    t = acha(e[1], e[0])
    if t is not None and abs(t - e[0]) > 0.3: print(f"[2] {e[1]:<14} {e[0]:8.1f} -> {t:8.1f}"); e[0] = round(t + 0.1, 2)
json.dump(P, open(PJ, "w"), ensure_ascii=False, indent=1)
print("ok")
