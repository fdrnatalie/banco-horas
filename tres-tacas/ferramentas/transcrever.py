"""Transcrição com tempo por palavra (faster-whisper large-v3-turbo).

uso: python3 transcrever.py video.mov saida.json [--hesitacoes]

Saída: lista de segmentos {s, e, t, words: [{w, s, e, p}]}, tempos em segundos do arquivo original.
--hesitacoes mantém ééé/hum/ahn/tosse (usado para limpar as falas, ver cleanfala.py).
"""
import sys, json, subprocess
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
hes = "--hesitacoes" in sys.argv
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     stdout=subprocess.PIPE, check=True).stdout
x = np.frombuffer(raw, np.float32)
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
kw = dict(language="pt", word_timestamps=True, vad_filter=False)
if hes:
    kw.update(initial_prompt="Ééé... hum... ahn... é... Então, ééé, eu vou, hum, colocar... ahn... (tosse) Ééé, tá.",
              condition_on_previous_text=False)
segs, _ = m.transcribe(x, **kw)
res = []
for s in segs:
    res.append(dict(s=round(s.start, 2), e=round(s.end, 2), t=s.text.strip(),
                    words=[dict(w=w.word, s=round(w.start, 2), e=round(w.end, 2), p=round(w.probability, 2)) for w in s.words]))
    print(f"{s.start:7.1f} {s.text.strip()[:70]}", flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False)
