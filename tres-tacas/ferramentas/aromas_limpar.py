"""Tira pausas (VAD) e trechos escolhidos de um vídeo vertical, acelera, e remapeia os tempos do placar.

uso: python3 aromas_limpar.py placar.json cortes.json saida.mp4 placar_saida.json
cortes.json: {"velocidade": 1.2, "cortes": [[a, b], ...]}  (tempos do vídeo de entrada)
"""
import sys, json, subprocess
import numpy as np
from faster_whisper.vad import get_speech_timestamps, VadOptions

P = json.load(open(sys.argv[1])); C = json.load(open(sys.argv[2])); OUT, POUT = sys.argv[3], sys.argv[4]
VID = P["video"]; SP = C.get("velocidade", 1.2)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", VID, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                 stdout=subprocess.PIPE, check=True).stdout, np.float32)
ts = get_speech_timestamps(x, VadOptions(threshold=0.5, min_silence_duration_ms=220, speech_pad_ms=90, min_speech_duration_ms=120))
segs = [[t["start"] / 16000, t["end"] / 16000] for t in ts]
for e in P["rodada1"] + [r for r in P.get("rodada2", []) if r[1] != "*"]:   # nunca perde um nome, mesmo falado baixinho
    segs.append([max(0, e[0] - 0.75), e[0] + 0.2])
segs.sort(); fund = []
for s0, e0 in segs:
    if fund and s0 <= fund[-1][1] + 0.05: fund[-1][1] = max(fund[-1][1], e0)
    else: fund.append([s0, e0])
segs = fund
for a, b in C.get("cortes", []):                       # subtrai os cortes
    out = []
    for s, e in segs:
        if e <= a or s >= b: out.append([s, e])
        else:
            if s < a: out.append([s, a])
            if e > b: out.append([b, e])
    segs = out
segs = [s for s in segs if s[1] - s[0] > 0.12]
if SP == "auto":                                       # velocidade para a 1ª rodada caber no alvo (1,15x a 1,5x)
    r1 = sum(min(e, P["fim_rodada1"]) - s for s, e in segs if s < P["fim_rodada1"])
    SP = round(min(1.5, max(1.15, r1 / C.get("alvo_rodada1", 88))), 3); print("velocidade", SP, "fala na 1ª rodada", round(r1, 1))
def mapa(t):
    acc = 0.0
    for s, e in segs:
        if t < s: return acc / SP
        if t <= e: return (acc + t - s) / SP
        acc += e - s
    return acc / SP
sel = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in segs)
vf = f"select='{sel}',setpts=N/FRAME_RATE/TB/{SP},fps=30"
if C.get("espelhar"): vf += ",hflip"                  # imagem espelhada (rosto do outro lado das listas)
af = f"aselect='{sel}',asetpts=N/SR/TB,atempo={SP},loudnorm=I=-14:TP=-1.5:LRA=9"
import os
if not os.path.exists(OUT) or "--refazer" in sys.argv:  # vídeo limpo já pronto: só remapeia os tempos
  subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VID, "-vf", vf, "-af", af, "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", OUT], check=True)
Q = dict(P); Q["video"] = OUT; Q["fim_rodada1"] = round(mapa(P["fim_rodada1"]), 2)
Q["rodada1"] = [[round(mapa(e[0]), 2)] + e[1:] for e in P["rodada1"]]
Q["rodada2"] = [[round(mapa(e[0]), 2)] + e[1:] for e in P["rodada2"]]; Q["velocidade"] = SP
json.dump(Q, open(POUT, "w"), ensure_ascii=False, indent=1)
print("ok", len(segs), "trechos; rodada 1 =", Q["fim_rodada1"], "s; total =", round(mapa(1e9), 1), "s")
