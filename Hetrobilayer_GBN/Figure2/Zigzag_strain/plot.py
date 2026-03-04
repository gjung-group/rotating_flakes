#!/usr/bin/env python3
"""Short processor: load three files, filter 0-4°, renormalize to AA, plot."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# ---- EDIT THESE ----
DATA_DIR = Path("/Users/jharaplaprathap/Desktop/FLakes/GBN/straindat/Armchair")
FILES = {
    "AA Total Energy": "E_inter_energy500P.dat",
    "AB1 Total Energy": "E_inter_energy500.dat",
    "AB Total Energy": "E_inter_energy500N.dat",
}


# epsilon values to SHOW in labels
EPS = {
    "AA": -0.008,
    "AB1": -0.018,
    "AB": -0.028,
}

ANGLE_MIN, ANGLE_MAX = 0.0, 4.0
# --------------------

def load_xy(p):
    a = np.genfromtxt(str(p))
    if a.ndim == 1:
        return a[:1].astype(float), a[1:2].astype(float)
    return a[:,0].astype(float), a[:,1].astype(float)

datasets, first = {}, {}
for label, fname in FILES.items():
    p = DATA_DIR / fname
    if not p.exists():
        print(f"Missing: {p}; skipping.")
        continue
    x, y = load_xy(p)
    mask = (x >= ANGLE_MIN) & (x <= ANGLE_MAX)
    x, y = x[mask], y[mask]
    if x.size == 0:
        print(f"No points in range for {label}; skipping.")
        continue
    datasets[label] = (x, y)
    first[label] = float(y[0])
    print(f"{label}: {x.size} pts, first_y={first[label]:.6g}")

if "AA Total Energy" not in first:
    raise SystemExit("AA Total Energy missing — cannot renormalize.")

ref = first["AA Total Energy"]
processed = {}
for label, (x,y) in datasets.items():
    y0 = first[label]
    y_sub = y - y0
    scale = (y0 / ref) if ref != 0 else 1.0
    processed[label] = (x, y_sub * scale)

# Plot stacked subplots
plt.rcParams.update({"font.family":"Times New Roman","font.size":12})
n = len(processed)
fig, axes = plt.subplots(n, 1, sharex=True, figsize=(6, 2.2*max(1,n)), dpi=200)
if n == 1: axes = [axes]
for ax, (label, (x,y)) in zip(axes, processed.items()):
    ax.plot(x, y, linewidth=1.5)
    ax.set_ylabel("ΔEnergy_inter meV/atom)")

    ax.grid(alpha=0.4, linestyle=":")
axes[-1].set_xlabel("Twist angle (°)")
axes[-1].set_xlim(ANGLE_MIN, ANGLE_MAX)
plt.tight_layout()
plt.show()

