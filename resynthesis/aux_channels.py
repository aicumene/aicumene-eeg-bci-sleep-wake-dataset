"""Regenerate the auxiliary PSG channels as physiologically plausible,
stage-conditioned surrogates (EEG derivations are left untouched, so BOID is
unchanged). EOG carries saccades in wake and rapid eye movements in REM; EMG is
a rectified envelope with tone highest in wake and minimal (atonia) in REM;
respiration is a slow oscillation; body temperature drifts within ~36.5-37.2 C.

Usage:  python aux_channels.py <dir> [record_id ...]
Requires MNE (to read the paired hypnogram annotations).
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
import mne

mne.set_log_level("ERROR")

EPOCH = 30.0
FS = 100.0
STAGE = {"Sleep stage W": "W", "Sleep stage 1": "N1", "Sleep stage 2": "N2",
         "Sleep stage 3": "N3", "Sleep stage 4": "N3", "Sleep stage R": "REM"}
# channel -> (phys_min, phys_max, dig_min, dig_max)
CAL = {2: (-1000.0, 1000.0, -2048, 2047),   # EOG uV
       3: (-1000.0, 1000.0, -2048, 2047),   # Resp a.u.
       4: (-100.0, 100.0, -2048, 2047),     # EMG uV (rectified envelope)
       5: (34.0, 40.0, -2048, 2047),        # Temp degC
       6: (0.0, 1.0, 0, 1)}                  # Marker


def _f(s, n):
    return (str(s) + " " * n)[:n].encode("latin1")


def _hdr(raw):
    ns = int(raw[252:256]); nrec = int(raw[236:244]); hb = int(raw[184:192])
    o = 256 + ns * (16 + 80 + 8 + 8 + 8 + 8 + 8 + 80)
    spr = [int(raw[o + i * 8:o + (i + 1) * 8]) for i in range(ns)]
    rsize = sum(spr); off = list(np.cumsum([0] + spr[:-1]))
    return ns, nrec, hb, spr, off, rsize


def _p2d(p, cal):
    pmin, pmax, dmin, dmax = cal
    d = np.round((np.asarray(p, float) - pmin) * (dmax - dmin) / (pmax - pmin) + dmin)
    return np.clip(d, dmin, dmax).astype("<i2")


def _stages(hyp, nrec):
    a = mne.read_annotations(hyp)
    lab = ["?"] * nrec
    for on, du, de in zip(a.onset, a.duration, a.description):
        st = STAGE.get(de)
        if st is None:
            continue
        for e in range(max(int(round(on / EPOCH)), 0), min(int(round((on + du) / EPOCH)), nrec)):
            lab[e] = st
    return lab


def gen_emg(lab, rng):
    lvl = {"W": 28, "N1": 20, "N2": 14, "N3": 10, "REM": 4, "?": 16}
    return np.concatenate([max(lvl.get(s, 16) * (1 + 0.15 * rng.standard_normal()), 0.5)
                           * (1 + 0.35 * np.abs(rng.standard_normal(30))) for s in lab])


def gen_temp(nrec, rng):
    n = nrec * 30; t = np.arange(n) / max(n - 1, 1)
    w = np.cumsum(rng.standard_normal(n)) * 0.002; w -= w.mean()
    return np.clip(rng.uniform(36.7, 37.1) - 0.3 * np.sin(np.pi * t)
                   + 0.03 * rng.standard_normal(n) + np.clip(w, -0.2, 0.2), 36.0, 37.6)


def gen_resp(lab, rng):
    n = len(lab) * 30
    inc = 2 * np.pi * np.clip(0.22 + 0.03 * rng.standard_normal()
                              + 0.03 * np.sin(2 * np.pi * 0.008 * np.arange(n)), 0.15, 0.35)
    sp = np.repeat([{"W": 1.2, "N1": 1.0, "N2": 1.0, "N3": 1.05, "REM": 1.15}.get(s, 1.0)
                    for s in lab], 30)[:n]
    return 450 * sp * np.sin(np.cumsum(inc)) + 60 * rng.standard_normal(n)


def gen_eog(lab, rng):
    out = []
    for s in lab:
        n = 3000
        base = np.cumsum(rng.standard_normal(n)) * 2.0; base -= base.mean()
        seg = np.clip(base, -150, 150)
        if s == "W":
            for _ in range(int(rng.integers(0, 4))):
                p = int(rng.integers(0, n - 60))
                seg[p:p + 50] += rng.choice([-1, 1]) * rng.uniform(150, 350) * np.hanning(50)
        elif s == "REM":
            for _ in range(int(rng.integers(0, 3))):
                p = int(rng.integers(0, n - 120))
                seg[p:p + 100] += rng.choice([-1, 1]) * rng.uniform(120, 250) * np.sin(np.linspace(0, 3 * np.pi, 100))
        elif s == "N1":
            seg += 80 * np.sin(2 * np.pi * rng.uniform(0.2, 0.5) * np.arange(n) / FS + rng.uniform(0, 6))
        out.append(np.clip(seg, -980, 980))
    return np.concatenate(out)


def regen(psg, hyp, seed):
    raw = bytearray(open(psg, "rb").read())
    ns, nrec, hb, spr, off, rsize = _hdr(raw)
    lab = _stages(hyp, nrec); rng = np.random.default_rng(seed)
    arr = np.frombuffer(bytes(raw[hb:hb + nrec * rsize * 2]), dtype="<i2").reshape(nrec, rsize).copy()
    gens = {2: gen_eog(lab, rng), 3: gen_resp(lab, rng), 4: gen_emg(lab, rng),
            5: gen_temp(nrec, rng), 6: np.zeros(nrec * 30)}
    for i in (2, 3, 4, 5, 6):
        arr[:, off[i]:off[i] + spr[i]] = _p2d(gens[i], CAL[i]).reshape(nrec, spr[i])
        pmin, pmax, dmin, dmax = CAL[i]
        raw[984 + i * 8:984 + i * 8 + 8] = _f(int(pmin) if float(pmin).is_integer() else pmin, 8)
        raw[1040 + i * 8:1040 + i * 8 + 8] = _f(int(pmax) if float(pmax).is_integer() else pmax, 8)
        raw[1096 + i * 8:1096 + i * 8 + 8] = _f(dmin, 8)
        raw[1152 + i * 8:1152 + i * 8 + 8] = _f(dmax, 8)
    raw[hb:hb + nrec * rsize * 2] = arr.tobytes()
    open(psg, "wb").write(bytes(raw))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    d = sys.argv[1]
    ids = sys.argv[2:] or sorted(os.path.basename(p).replace("-PSG.edf", "")
                                 for p in glob.glob(f"{d}/*-PSG.edf"))
    order = sorted(os.path.basename(p).replace("-PSG.edf", "") for p in glob.glob(f"{d}/*-PSG.edf"))
    for rid in ids:
        regen(f"{d}/{rid}-PSG.edf", f"{d}/{rid}-Hypnogram.edf",
              seed=7777 + (order.index(rid) if rid in order else 0))
        print(f"regenerated aux: {rid}", flush=True)


if __name__ == "__main__":
    main()
