#!/usr/bin/env python3
"""
Plot θ_C vs lattice constant (a) using the "+" algebraic root,
only for α > 1 (i.e. a > a0).

Save as plot_theta_vs_a.py and run with Python 3.
Requires: numpy, scipy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MaxNLocator

# ---------------------------
# Materials: lattice constants (Å) + plot colors
# ---------------------------
materials = {
    "Graphene": {"a": 2.46, "color": (0.122, 0.467, 0.706)},
    "hBN": {"a": 2.504, "color": (1.000, 0.498, 0.055)},
    "Silicene": {"a": 3.079, "color": (0.173, 0.627, 0.173)},
    "TaS2": {"a": 3.30, "color": (0.498, 0.498, 0.498)},
    "MoS2": {"a": 3.169, "color": (0.090, 0.745, 0.811)},
    "WS2": {"a": 3.161, "color": (0.682, 0.780, 0.909)},
    "MoSe2": {"a": 3.283, "color": (1.000, 0.733, 0.470)},
    "WSe2": {"a": 3.285, "color": (0.596, 0.875, 0.541)},
    "NbSe2": {"a": 3.444, "color": (1.000, 0.596, 0.588)},
    "6H-SiC": {"a": 3.08, "color": (0.780, 0.780, 0.780)},
    "4H-SiC": {"a": 3.08, "color": (0.863, 0.863, 0.522)},
    "MoTe2": {"a": 3.519, "color": (0.620, 0.878, 0.898)},
}


# materials = {
#     "Graphene": {"a": 2.6, "color": (0.122, 0.467, 0.706)},
#     "hBN": {"a": 2.504, "color": (1.000, 0.498, 0.055)},
#     "Silicene": {"a": 3.079, "color": (0.173, 0.627, 0.173)},
#     "Germanene": {"a": 3.99, "color": (0.839, 0.153, 0.157)},
#     "GaSe": {"a": 3.755, "color": (0.580, 0.404, 0.741)},
#     "GaTe": {"a": 4.06, "color": (0.549, 0.337, 0.294)},
#     "SnS2": {"a": 3.645, "color": (0.890, 0.467, 0.761)},
#     "TaS2": {"a": 3.30, "color": (0.498, 0.498, 0.498)},
#     "MoS2": {"a": 3.169, "color": (0.090, 0.745, 0.811)},
#     "WS2": {"a": 3.161, "color": (0.682, 0.780, 0.909)},
#     "MoSe2": {"a": 3.283, "color": (1.000, 0.733, 0.470)},
#     "WSe2": {"a": 3.285, "color": (0.596, 0.875, 0.541)},
#     "NbSe2": {"a": 3.444, "color": (1.000, 0.596, 0.588)},
#     "HfS2": {"a": 3.56, "color": (0.773, 0.690, 0.835)},
#     "ZrS2": {"a": 3.68, "color": (0.769, 0.612, 0.580)},
#     "PtSe2": {"a": 3.731, "color": (0.984, 0.705, 0.824)},
#     "6H-SiC": {"a": 3.08, "color": (0.780, 0.780, 0.780)},
#     "4H-SiC": {"a": 3.08, "color": (0.863, 0.863, 0.522)},
#     "MoTe2": {"a": 3.519, "color": (0.620, 0.878, 0.898)},
#     "InSe": {"a": 4.05, "color": (0.450, 0.450, 0.450)}
# }


# Lattice sampling range (Å)
a_vals = np.linspace(2.0, 5.0, 1000)

# ---------------------------
# θC from the + algebraic root
# ---------------------------
def compute_theta(alpha):
    """
    alpha: scalar or numpy array
    returns theta in degrees using arg = (1 + sqrt(3(4alpha^2 - 1))) / (4 alpha)
    safely clips the argument to [-1, 1] before arccos.
    """
    alpha = np.asarray(alpha, dtype=float)
    # discriminant: 3(4 alpha^2 - 1) = -3 + 12 alpha^2
    disc_inner = -3.0 + 12.0 * alpha**2
    disc = np.sqrt(np.clip(disc_inner, 0.0, np.inf))
    arg = (1.0 + disc) / (4.0 * alpha)

    # numerical safety for arccos
    arg = np.clip(arg, -1.0, 1.0)
    theta_rad = np.arccos(arg)
    return np.degrees(theta_rad)


# ---------------------------
# Figure setup
# ---------------------------
fig = plt.figure(figsize=(8, 6), dpi=200)
gs = GridSpec(2, 1, height_ratios=[1, 5], hspace=0.02)

ax_label = fig.add_subplot(gs[0])
ax = fig.add_subplot(gs[1], sharex=ax_label)

# No grid lines (as requested)
ax.grid(False)

# Axis limits and labels
x_min, x_max = 2.35, 3.8
ax.set_xlim(x_min, x_max)
ax.set_ylim(0, 2.8)

ax.set_xlabel("a (Å)")
ax.set_ylabel(r"$\theta_A$ (degrees)")

# ---------------------------
# Plot every material (only where alpha > 1)
# ---------------------------
sorted_materials = sorted(materials.items(), key=lambda x: x[1]["a"])

for name, props in sorted_materials:
    a0 = float(props["a"])
    color = props["color"]

    # compute alpha for the full sampling
    alpha_full = 1.0 + (a_vals - a0) / a0

    # mask: only alpha > 1 (a > a0)
    mask = alpha_full > 1.0
    if not np.any(mask):
        # no valid region for this material in the sampling range
        continue

    a_masked = a_vals[mask]
    alpha_masked = alpha_full[mask]

    # compute theta only for the valid region
    theta = compute_theta(alpha_masked)

    # plot theta vs a (only for a > a0)
    ax.plot(a_masked, theta, color=color, label=name)

    # vertical line at a0
    ax.axvline(a0, linestyle="--", color=color, linewidth=0.7)

    # horizontal reference at alpha = 1 (theta when a = a0)
    # compute theta at alpha = 1 (scalar)
    theta_at_a0 = compute_theta(np.array([1.0]))[0]
    ax.plot([x_min, a0], [theta_at_a0, theta_at_a0],
            linestyle="--", color=color, linewidth=1.0)

# ---------------------------
# Axes formatting
# ---------------------------
ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
ax.yaxis.set_minor_locator(MaxNLocator(nbins=8))
ax.tick_params(axis="both", which="major", length=8, width=1.5)
ax.tick_params(axis="both", which="minor", length=4, width=1.2)

for spine in ax.spines.values():
    spine.set_linewidth(1.5)

ax_label.axis("off")
ax_label.set_xlim(ax.get_xlim())
ax_label.set_ylim(0, 1)

# Optional: legend (can be enabled/disabled)
ax.legend(loc="upper right", fontsize="small", frameon=False, ncol=1)

plt.tight_layout()
plt.show()

