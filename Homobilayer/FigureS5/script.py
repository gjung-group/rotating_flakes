#!/usr/bin/env python3
"""
fit_energy_vs_angle.py

Read energy vs angle and moiré metadata files, compute AA/AB contributions,
interpolate, fit a simple linear model (energy = a * diff + b), and plot the result.

Here E_inter_energy_D500II.dat is renormalized data by subtracting from the maximum energy from the data set .


Edit the FILE_* paths below to point at your data files.
"""

from __future__ import annotations
import numpy as np
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator

# ------------ User-editable paths ------------
FILE_ENERGY = Path("********************/E_inter_energy_D500II.dat")
FILE_MOIRE  = Path("********************/hBN_moire_Armcchair_500.dat")
# --------------------------------------------

# Constants
R = 500 * 2.50579           # radius in angstroms
E_AA = -13.0                # energy per AA atom (meV)
E_AB = -20.0                # energy per AB atom (meV)
ANGLE_MIN, ANGLE_MAX = 0.1, 10.0
INTERP_POINTS = 6000        # number of points for final interpolation
FIG_DPI = 300


def read_two_col(path: Path):
    data = np.genfromtxt(path)
    if data.size == 0:
        raise FileNotFoundError(f"No data in {path}")
    if data.ndim == 1:
        if data.size < 2:
            raise ValueError(f"File {path} must contain at least two columns")
        return np.array([data[0]]), np.array([data[1]])
    return data[:, 0], data[:, 1]


def area_hexagon(radius: float) -> float:
    return (3.0 * np.sqrt(3.0) / 2.0) * radius ** 2


def area_cell(moire_length: float) -> float:
    return (np.sqrt(3.0) / 2.0) * moire_length ** 2


def compute_n1m(num_points: float, moire_length: float, AmL: float, AmR: float) -> float:
    return num_points * (AmL / AmR)


def fit_func(x, a, b):
    return a * x + b


def main():
    # Load energy vs angle
    angles, energies = read_two_col(FILE_ENERGY)

    # Load moire metadata: expected columns [.., moire_length, n_AA, n_AB, ...]
    moire_data = np.genfromtxt(FILE_MOIRE)
    if moire_data.ndim == 1 and moire_data.size < 4:
        raise ValueError("moire file must contain at least 4 columns per row")
    moire_lengths = moire_data[:, 1]
    num_AA_points = moire_data[:, 2]
    num_AB_points = moire_data[:, 3]

    # Precompute areas
    AmR = area_hexagon(R)

    # Compute n1m and energies lists (for each moire entry)
    n1m_aa = []
    n1m_ab = []
    energy_aa = []
    energy_ab = []
    for aa, ab, ml in zip(num_AA_points, num_AB_points, moire_lengths):
        AmL = area_cell(ml)
        n1m_a = compute_n1m(aa, ml, AmL, AmR)
        n1m_b = compute_n1m(ab, ml, AmL, AmR)
        n1m_aa.append(n1m_a)
        n1m_ab.append(n1m_b)
        energy_aa.append(n1m_a * E_AA)
        energy_ab.append(n1m_b * (E_AB * 2.0)) (twice because E_AB and E_BA are equall for homobialyers)

    n1m_aa = np.array(n1m_aa)
    n1m_ab = np.array(n1m_ab)
    energy_aa = np.array(energy_aa)
    energy_ab = np.array(energy_ab)

    diff_AA_AB = energy_aa - energy_ab  # same length as moire_data

    # Filter energy data by angle range
    mask = (angles >= ANGLE_MIN) & (angles <= ANGLE_MAX)
    angles_f = angles[mask]
    energies_f = energies[mask]

    # Make sure diff array aligns to angles. If lengths match, use directly; else interpolate diff -> angles
    if len(diff_AA_AB) == len(angles):
        diff_f = diff_AA_AB[mask]
    else:
        # interpolate diff as function of moire_length to angles_f using nearest mapping if possible
        # fallback: linearly interpolate diff vs moire_lengths to the angle grid range
        try:
            interp_diff_map = interp1d(moire_lengths, diff_AA_AB, kind="linear", fill_value="extrapolate")
            diff_f = interp_diff_map(angles_f)
        except Exception:
            # last resort: trim or pad
            L = min(len(diff_AA_AB), len(angles_f))
            diff_f = np.resize(diff_AA_AB, angles_f.shape)[:L]
            if len(diff_f) < len(angles_f):
                diff_f = np.pad(diff_f, (0, len(angles_f) - len(diff_f)), mode="edge")

    # Interpolate both series to common dense grid for fitting & plotting
    interp_angles = np.linspace(np.min(angles_f), np.max(angles_f), INTERP_POINTS)
    interp_energies = interp1d(angles_f, energies_f, kind="linear", fill_value="extrapolate")(interp_angles)
    interp_diff = interp1d(angles_f, diff_f, kind="linear", fill_value="extrapolate")(interp_angles)

    # Fit linear model: energy = a * diff + b
    popt, pcov = curve_fit(fit_func, interp_diff, interp_energies)
    a, b = popt
    fitted = fit_func(interp_diff, a, b)

    # Plot
    plt.rcParams.update({
        "font.family": "Times New Roman",
        "font.size": 14,
        "lines.linewidth": 2.5
    })
    fig, ax = plt.subplots(figsize=(8, 6), dpi=FIG_DPI)
    ax.plot(interp_angles, interp_energies, color="black", label="Energy (interp)")
    ax.plot(interp_angles, fitted, color="red", label=f"Fit: E = {a:.4e}*diff + {b:.4e}")
    ax.set_xlim(0.1, 3.0)
    ax.tick_params(axis="both", which="major", length=8, width=1.2)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
    ax.set_xlabel("Angle (degrees)")
    ax.set_ylabel("Energy (meV)")
    ax.legend()
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    plt.tight_layout()
    plt.show()

    # Print results
    print(f"Fitting parameters: a = {a:.6e}, b = {b:.6e}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
fit_energy_vs_angle.py

Read energy vs angle and moiré metadata files, compute AA/AB contributions,
interpolate, fit a simple linear model (energy = a * diff + b), and plot the result.

Edit the FILE_* paths below to point at your data files.
"""

from __future__ import annotations
import numpy as np
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator

# ------------ User-editable paths ------------
FILE_ENERGY = Path("*****/E_inter_energy_D500II.dat") ####renormalized data by subtracting the max energy from E_inter_energy_D500I.dat
FILE_MOIRE  = Path("hBN_moire_Armcchair_500.dat")    ###using SC method
# --------------------------------------------

# Constants
R = 500 * 2.50579           # radius in angstroms
E_AA = -13.0                # energy per AA atom (meV)
E_AB = -20.0                # energy per AB atom (meV)
ANGLE_MIN, ANGLE_MAX = 0.1, 10.0
INTERP_POINTS = 6000        # number of points for final interpolation
FIG_DPI = 300


def read_two_col(path: Path):
    data = np.genfromtxt(path)
    if data.size == 0:
        raise FileNotFoundError(f"No data in {path}")
    if data.ndim == 1:
        if data.size < 2:
            raise ValueError(f"File {path} must contain at least two columns")
        return np.array([data[0]]), np.array([data[1]])
    return data[:, 0], data[:, 1]


def area_hexagon(radius: float) -> float:
    return (3.0 * np.sqrt(3.0) / 2.0) * radius ** 2


def area_cell(moire_length: float) -> float:
    return (np.sqrt(3.0) / 2.0) * moire_length ** 2


def compute_n1m(num_points: float, moire_length: float, AmL: float, AmR: float) -> float:
    return num_points * (AmL / AmR)


def fit_func(x, a, b):
    return a * x + b


def main():
    # Load energy vs angle
    angles, energies = read_two_col(FILE_ENERGY)

    # Load moire metadata: expected columns [.., moire_length, n_AA, n_AB, ...]
    moire_data = np.genfromtxt(FILE_MOIRE)
    if moire_data.ndim == 1 and moire_data.size < 4:
        raise ValueError("moire file must contain at least 4 columns per row")
    moire_lengths = moire_data[:, 1]
    num_AA_points = moire_data[:, 2]
    num_AB_points = moire_data[:, 3]

    # Precompute areas
    AmR = area_hexagon(R)

    # Compute n1m and energies lists (for each moire entry)
    n1m_aa = []
    n1m_ab = []
    energy_aa = []
    energy_ab = []
    for aa, ab, ml in zip(num_AA_points, num_AB_points, moire_lengths):
        AmL = area_cell(ml)
        n1m_a = compute_n1m(aa, ml, AmL, AmR)
        n1m_b = compute_n1m(ab, ml, AmL, AmR)
        n1m_aa.append(n1m_a)
        n1m_ab.append(n1m_b)
        energy_aa.append(n1m_a * E_AA)
        energy_ab.append(n1m_b * (E_AB * 2.0))

    n1m_aa = np.array(n1m_aa)
    n1m_ab = np.array(n1m_ab)
    energy_aa = np.array(energy_aa)
    energy_ab = np.array(energy_ab)

    diff_AA_AB = energy_aa - energy_ab  # same length as moire_data

    # Filter energy data by angle range
    mask = (angles >= ANGLE_MIN) & (angles <= ANGLE_MAX)
    angles_f = angles[mask]
    energies_f = energies[mask]

    # Make sure diff array aligns to angles. If lengths match, use directly; else interpolate diff -> angles
    if len(diff_AA_AB) == len(angles):
        diff_f = diff_AA_AB[mask]
    else:
        # interpolate diff as function of moire_length to angles_f using nearest mapping if possible
        # fallback: linearly interpolate diff vs moire_lengths to the angle grid range
        try:
            interp_diff_map = interp1d(moire_lengths, diff_AA_AB, kind="linear", fill_value="extrapolate")
            diff_f = interp_diff_map(angles_f)
        except Exception:
            # last resort: trim or pad
            L = min(len(diff_AA_AB), len(angles_f))
            diff_f = np.resize(diff_AA_AB, angles_f.shape)[:L]
            if len(diff_f) < len(angles_f):
                diff_f = np.pad(diff_f, (0, len(angles_f) - len(diff_f)), mode="edge")

    # Interpolate both series to common dense grid for fitting & plotting
    interp_angles = np.linspace(np.min(angles_f), np.max(angles_f), INTERP_POINTS)
    interp_energies = interp1d(angles_f, energies_f, kind="linear", fill_value="extrapolate")(interp_angles)
    interp_diff = interp1d(angles_f, diff_f, kind="linear", fill_value="extrapolate")(interp_angles)

    # Fit linear model: energy = a * diff + b
    popt, pcov = curve_fit(fit_func, interp_diff, interp_energies)
    a, b = popt
    fitted = fit_func(interp_diff, a, b)

    # Plot
    plt.rcParams.update({
        "font.family": "Times New Roman",
        "font.size": 14,
        "lines.linewidth": 2.5
    })
    fig, ax = plt.subplots(figsize=(8, 6), dpi=FIG_DPI)
    ax.plot(interp_angles, interp_energies, color="black", label="Energy (interp)")
    ax.plot(interp_angles, fitted, color="red", label=f"Fit: E = {a:.4e}*diff + {b:.4e}")
    ax.set_xlim(0.1, 3.0)
    ax.tick_params(axis="both", which="major", length=8, width=1.2)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
    ax.set_xlabel("Angle (degrees)")
    ax.set_ylabel("Energy (meV)")
    ax.legend()
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
    plt.tight_layout()
    plt.show()

    # Print results
    print(f"Fitting parameters: a = {a:.6e}, b = {b:.6e}")


if __name__ == "__main__":
    main()

