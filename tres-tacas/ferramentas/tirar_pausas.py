"""Vídeo vertical da câmera: tira as pausas (e ruídos sem fala, como cantarolar ao fundo), sem cortar fala e sem texto.

uso: python3 tirar_pausas.py entrada.mov saida.mp4 [velocidade=1.1]
Mantém só os trechos com palavras (transcrição com tempo por palavra), com folga curta antes e depois;
vídeo e áudio cortados juntos quadro a quadro (sem dessincronizar).
"""
import sys, os, json, subprocess
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]; speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.1
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], stdout=subprocess.PIPE, check=True).stdout
x = np.frombuffer(raw, np.float32)
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
segs, _ = m.transcribe(x, language="pt", word_timestamps=True, vad_filter=False)
words = [(w.start, w.end, w.word) for s in segs for w in s.words if w.word.strip(".,!?…;: ") and w.probability > 0.25]
json.dump(words, open(os.path.splitext(out)[0] + "_palavras.json", "w"), ensure_ascii=False)
PAD0, PAD1, GAP = 0.10, 0.18, 0.40
keep = []
for a, b, _ in words:
    a, b = max(0, a - PAD0), b + PAD1
    if keep and a - keep[-1][1] < GAP: keep[-1][1] = max(keep[-1][1], b)
    else: keep.append([a, b])
keep = [(a, b) for a, b in keep if b - a > 0.25]
sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
vf = f"select='{sel}',setpts=N/FRAME_RATE/TB/{speed},scale=1080:1920,fps=30"
af = (f"aselect='{sel}',asetpts=N/SR/TB,highpass=f=75,afftdn=nr=10:nf=-40,"
      f"acompressor=threshold=0.08:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=8,atempo={speed}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", out, "-frames:v", "1", "-vf", "scale=432:-2", os.path.splitext(out)[0] + "_capa.jpg"], check=True)
tot = sum(b - a for a, b in keep)
print(f"ok {out}: {len(keep)} trechos, {tot / speed:.1f}s de {len(x) / 16000:.1f}s", flush=True)
