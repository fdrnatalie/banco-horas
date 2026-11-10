"""split a spoken range [a, b] into clean sub-ranges: drop fillers (ééé/hum/ahn, long 'é'), coughs and pauses between words.
words come from the full raw transcript (T); disfluencies from the filler-aware pass (F); energy confirms what sits in each gap."""
import json, re, wave
import numpy as np

FILL = re.compile(r"^(é{2,}|eh+|e{3,}|hum+|hm+|ahn+|ah+|uh+|mm+|\(?tosse\)?)[.,!?…]*$", re.I)

class Cleaner:
    def __init__(self, trans, fillers, audio):
        self.W = [w for s in json.load(open(trans)) for w in s["words"]]
        self.F = []
        for s in json.load(open(fillers)):
            for w in s["words"]:
                t = w["w"].strip().lower()
                if FILL.match(t) or (t.strip(".,…") == "é" and w["e"] - w["s"] > 0.45): self.F.append((w["s"], w["e"]))
        wv = wave.open(audio); self.sr = wv.getframerate(); n = wv.getnframes(); ch = wv.getnchannels()
        x = np.frombuffer(wv.readframes(n), np.int16).astype(np.float32) / 32768
        if ch > 1: x = x.reshape(-1, ch).mean(1)
        hop = self.sr // 100; k = len(x) // hop
        self.rms = np.sqrt((x[:k * hop].reshape(k, hop) ** 2).mean(1) + 1e-12)      # 10 ms frames

    def voiced(self, a, b):
        i, j = int(a * 100), int(b * 100)
        if j <= i: return 0.0
        r = self.rms[i:j]; floor = np.percentile(self.rms, 30) * 3
        return float((r > floor).mean())

    def clean(self, a, b, gap=0.32, pad=0.08, tail=0.15):
        ws = [w for w in self.W if a - 0.05 <= (w["s"] + w["e"]) / 2 <= b + 0.05]
        if not ws: return [(a, b)], []
        ws = [w for w in ws if not FILL.match(w["w"].strip().lower())]
        out, dropped = [], []
        cur_a = max(a, ws[0]["s"] - pad); last_e = ws[0]["e"]
        for w in ws[1:]:
            g0, g1 = last_e, w["s"]
            filler = any(fs < g1 and fe > g0 for fs, fe in self.F)
            if g1 - g0 > gap or (filler and g1 - g0 > 0.15):
                out.append((cur_a, g0 + pad)); dropped.append((round(g0, 2), round(g1, 2), "filler" if filler else ("voz" if self.voiced(g0, g1) > 0.4 else "pausa")))
                cur_a = g1 - pad
            last_e = w["e"]
        out.append((cur_a, min(b, last_e + tail)))
        # a filler swallowed inside a long word (whisper stretches the word over the 'ééé'): cut the filler span out
        res = []
        for p, q in out:
            segs = [(p, q)]
            for fs, fe in self.F:
                nxt = []
                for s_, e_ in segs:
                    if fe <= s_ or fs >= e_ or fe - fs < 0.3: nxt.append((s_, e_)); continue
                    if fs - s_ > 0.12: nxt.append((s_, fs))
                    if e_ - fe > 0.12: nxt.append((fe, e_))
                    dropped.append((round(fs, 2), round(fe, 2), "filler"))
                segs = nxt
            res += segs
        return [(round(p, 3), round(q, 3)) for p, q in res if q - p > 0.12], dropped
