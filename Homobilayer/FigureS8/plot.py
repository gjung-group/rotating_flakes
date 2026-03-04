#!/usr/bin/env python3
"""
plot_flake_rotations.py

Minimal, clean script to produce a publication-quality PDF of per-atom
rotation angles for a flake. The script reads:
 - <base>/generateInit.xyz
 - <base>/rotation_angles.txt

It builds the base path from the initial angle value (formatted to 2 decimals).
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib import rcParams

# Matplotlib settings (publication style)
rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 20,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "figure.dpi": 300,
    "axes.linewidth": 1.2,
    "xtick.direction": 'in',
    "ytick.direction": 'in',
    "xtick.major.size": 6,
    "ytick.major.size": 6,
})


def read_xyz(file_path: Path, header_lines: int = 2) -> np.ndarray:
    """Read an .xyz and return Nx3 array of floats (x,y,z)."""
    if not file_path.exists():
        raise FileNotFoundError(f"XYZ file not found: {file_path}")
    positions = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[header_lines:]
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4:
            # allow element label + x y z (or arbitrary first column)
            _, x, y, z = parts[:4]
            positions.append([float(x), float(y), float(z)])
    return np.asarray(positions)


def main(initial_angle: float = 0.62, center_angle: float = 0.647):
    """
    initial_angle : float
        The reference initial twist (used to build folder name).
    center_angle : float
        Center value for TwoSlopeNorm (the color center).
    """

    ref_str = f"{initial_angle:.2f}"
    base_dir = Path(
        f"********************************************/{ref_str}"
    )
    init_xyz = base_dir / "generateInit.xyz"
    rot_txt = base_dir / "rotation_angles.txt"
    out_pdf = Path(f"flake_rotation_{initial_angle:.2f}.pdf")

    # constants
    z_flake = 19.175
    tol = 1e-3

    # --- read inputs
    pos_all = read_xyz(init_xyz)          # Nx3
    if not rot_txt.exists():
        raise FileNotFoundError(f"Rotation angle file not found: {rot_txt}")
    rot_data = np.loadtxt(rot_txt)
    if rot_data.ndim == 1:
        rot_data = rot_data.reshape(1, -1)

    # select flake atoms by z
    flake_mask = np.isclose(pos_all[:, 2], z_flake, atol=tol)
    flake_positions = pos_all[flake_mask]
    if flake_positions.size == 0:
        raise RuntimeError("No flake atoms found at the specified z value.")

    # rotation angles: assume rotation file has at least two columns (index, angle)
    angles_all = rot_data[:, 1]
    if len(angles_all) < len(flake_positions):
        raise RuntimeError("Not enough rotation angles for flake atom count.")

    # map angles to flake atoms (take first N)
    flake_angles = angles_all[: len(flake_positions)]
    final_angles = flake_angles + initial_angle

    # filter for display (keep angles within ±5 deg of zero by default)
    display_mask = (final_angles > -5.0) & (final_angles < 5.0)
    display_positions = flake_positions[display_mask]
    display_angles = final_angles[display_mask]

    if display_positions.size == 0:
        raise RuntimeError("No atoms remain after filtering angles for plotting.")

    x = display_positions[:, 0]
    y = display_positions[:, 1]
    c = display_angles

    # color normalization: use fixed vmin/vmax for consistent database visuals
    vmin, vmax = 0.55, 0.86
    norm = TwoSlopeNorm(vmin=vmin, vcenter=center_angle, vmax=vmax)

    # plotting (save only)
    plt.figure(figsize=(7, 6), dpi=300)
    sc = plt.scatter(x, y, c=c, cmap='seismic', s=8, norm=norm, marker='h', edgecolors='none')
    cb = plt.colorbar(sc, pad=0.02, aspect=40)
    cb.ax.tick_params(direction='out')
    plt.gca().set_xticklabels([])
    plt.gca().set_yticklabels([])
    cb.ax.set_yticklabels([])

    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(out_pdf, bbox_inches='tight')
    plt.close()
    print(f"Saved plot: {out_pdf}")


if __name__ == "__main__":
    # default call; change values when calling from database or wrapper
    main(initial_angle=0.62, center_angle=0.647)

