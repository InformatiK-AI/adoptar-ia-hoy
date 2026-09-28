"""Build assets/audio/soundtrack.wav: a synthesized music bed + SFX cues, pre-mixed.

Deterministic (no randomness), royalty-free. The bed stays low because Gonzalo narrates live.
Cue times match the beats in index.html / BRIEF.md.

  python tools/make_audio.py
"""
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 44100
DUR = 120.0
HERE = Path(__file__).resolve().parent.parent
SFX_DIR = HERE / "assets" / "sfx"
OUT = HERE / "assets" / "audio" / "soundtrack.wav"

N = int(SR * DUR)
t = np.arange(N) / SR


def hz(note):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    name, octave = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[name] + 12 * (octave - 4)) / 12)


def lowpass(x, cutoff):
    from scipy.signal import lfilter
    a = np.exp(-2 * np.pi * cutoff / SR)
    return lfilter([1 - a], [1, -a], x)  # one-pole low-pass


def env(start, end, attack, release):
    e = np.zeros(N)
    s, e_i = int(start * SR), int(min(end, DUR) * SR)
    seg = np.arange(e_i - s) / SR
    shape = np.minimum(1, seg / attack) * np.minimum(1, (end - start - seg) / release)
    e[s:e_i] = np.clip(shape, 0, 1)
    return e


# (start, end, notes) — D minor tension -> Bb/F learning -> Gm/A build -> D major resolution
CHORDS = [
    (0, 24.5, ["D2", "D3", "F3", "A3"]),
    (24, 40.5, ["A#1", "A#2", "D3", "F3"]),
    (40, 56.5, ["F2", "F3", "A3", "C4"]),
    (56, 70.5, ["G1", "G2", "A#3", "D4"]),
    (70, 77.6, ["A1", "A2", "C#4", "E4"]),
    (77.3, 98.5, ["D2", "D3", "F#3", "A3"]),
    (98, 108.5, ["G1", "G2", "B3", "D4"]),
    (108, 120, ["D2", "D3", "F#3", "A3", "D4"]),
]

pad = np.zeros(N)
for start, end, notes in CHORDS:
    e = env(start, end, 1.6, 1.8)
    for k, n in enumerate(notes):
        f = hz(n)
        for det in (-0.12, 0.12):  # gentle chorus
            ff = f * 2 ** (det / 12)
            voice = np.sin(2 * np.pi * ff * t) + 0.35 * np.sin(4 * np.pi * ff * t) + 0.12 * np.sin(6 * np.pi * ff * t)
            pad += e * voice * (0.9 if k == 0 else 0.55)
pad = lowpass(pad, 1400)
pad *= 0.9 + 0.1 * np.sin(2 * np.pi * 0.11 * t)  # slow swell

# Clock tick during beat 1 (SLA ticking): filtered click every 0.5 s
tick = np.zeros(N)
click = np.sin(2 * np.pi * 2200 * np.arange(int(0.012 * SR)) / SR) * np.exp(-np.arange(int(0.012 * SR)) / (0.003 * SR))
for i, s in enumerate(np.arange(0.5, 23.0, 0.5)):
    j = int(s * SR)
    tick[j:j + len(click)] += click * (1.0 if i % 2 == 0 else 0.6)

# Plucked arpeggio (100 bpm eighths) from 26 s to 108 s, following the chord roots
arp = np.zeros(N)
step = 60 / 100 / 2
pluck_len = int(0.6 * SR)
pt = np.arange(pluck_len) / SR
for s in np.arange(26.0, 107.9, step):
    chord = [c for c in CHORDS if c[0] <= s < c[1]][-1][2]
    tones = [hz(n) * (2 if s >= 77.3 else 1) for n in chord[1:]]
    f = tones[int(round((s - 26.0) / step)) % len(tones)] * 2
    j = int(s * SR)
    p = (np.sin(2 * np.pi * f * pt) + 0.3 * np.sin(4 * np.pi * f * pt)) * np.exp(-pt / 0.16)
    arp[j:j + pluck_len] += p[: N - j]
arp *= np.clip((t - 26) / 4, 0, 1) * np.clip((108.5 - t) / 1.5, 0, 1)

bed = pad / np.max(np.abs(pad)) * 0.20 + tick * 0.05 + arp / np.max(np.abs(arp)) * 0.07


def load_sfx(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SFX_DIR / f"{name}.mp3"), "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0


# (time_s, sfx, gain). Riser is placed so it ends on the answer hit at 77.3 s.
CUES = [
    (7.0, "notification", 0.55), (10.5, "notification", 0.35), (12.0, "notification", 0.35),
    (15.0, "whoosh-short", 0.35), (16.2, "impact-bass-1", 0.35),
    (24.0, "whoosh-cinematic", 0.40), (31.6, "whoosh-short", 0.30),
    (39.8, "sparkle", 0.30), (47.1, "whoosh-cinematic", 0.40), (48.6, "sparkle", 0.25),
    (55.8, "whoosh-short", 0.30), (57.0, "typing", 0.22), (58.6, "typing", 0.22), (60.2, "typing", 0.22),
    (61.8, "typing", 0.22), (66.2, "ping", 0.40),
    (70.5, "pop", 0.25), (71.1, "pop", 0.25), (71.7, "pop", 0.25), (72.3, "pop", 0.25),
    (77.3, "impact-bass-1", 0.45), (87.7, "whoosh-cinematic", 0.40),
    (89.0, "whoosh-short", 0.22), (90.0, "whoosh-short", 0.22), (91.0, "whoosh-short", 0.22),
    (92.0, "whoosh-short", 0.22), (93.0, "whoosh-short", 0.22),
    (96.3, "click-soft", 0.45), (97.5, "click-soft", 0.45), (98.7, "click-soft", 0.45), (99.9, "click-soft", 0.45),
    (101.1, "click-soft", 0.45), (102.5, "chime", 0.35),
    (107.7, "whoosh-cinematic", 0.35), (108.4, "typing", 0.18), (110.0, "typing", 0.18), (113.5, "chime", 0.40),
]
sfx = np.zeros(N)
cache = {}
riser = load_sfx("riser")
j = int((77.3 - len(riser) / SR) * SR)
sfx[j:j + len(riser)] += riser * 0.30
for at, name, gain in CUES:
    x = cache.setdefault(name, load_sfx(name))
    j = int(at * SR)
    n = min(len(x), N - j)
    sfx[j:j + n] += x[:n] * gain

mix = bed + sfx
mix *= np.clip(t / 0.8, 0, 1) * np.clip((DUR - t) / 2.5, 0, 1)  # fade in/out
peak = np.max(np.abs(mix))
mix = mix / peak * 0.63  # ~ -4 dBFS peak, ~ -20 LUFS: sits under a live voice
stereo = np.repeat((mix * 32767).astype(np.int16)[:, None], 2, axis=1)
OUT.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(OUT), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(stereo.tobytes())
print(f"wrote {OUT} ({DUR:.0f}s, peak before norm {peak:.2f})")
