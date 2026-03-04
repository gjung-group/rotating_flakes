#!/usr/bin/env python3
"""clean_moire_fit.py

Minimal, clean script to load two data files, compute the domain-energy metric,
fit a linear model, and plot the result. Edit the file paths below as needed.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

# --- User-editable paths and constants ------------------------------------
ENERGY_FILE = '******************/E_inter_energy.dat'
AB_FILE = '**********************/Zigzag_GBN.dat'
R = 500.0 * 2.50579  # reference radius (Å)
E_AA, E_AB, E_BA = -18.0, -19.0, -23.0  # meV/atom

# --- Helpers ---------------------------------------------------------------
def area_hexagon(r):
    return (3 * np.sqrt(3) / 2) * r**2

def area_cell(L):
    return (np.sqrt(3) / 2) * L**2

def linear(x, a, b):
    return a * x + b

# --- Load data ------------------------------------------------------------
energy_data = np.loadtxt(ENERGY_FILE)
ab_data = np.loadtxt(AB_FILE)

angles = energy_data[:, 0]
energies = energy_data[:, 1]

moire_lengths = ab_data[:, 1]
n_AA = ab_data[:, 2]
n_AB = ab_data[:, 3]
n_BA = ab_data[:, 4]

# --- Compute metric ------------------------------------------------------
AmR = area_hexagon(R)
AmL = area_cell(moire_lengths)

n1m_AA = n_AA * (AmL / AmR)
n1m_AB = n_AB * (AmL / AmR)
n1m_BA = n_BA * (AmL / AmR)

energy_AA = n1m_AA * E_AA
energy_AB = n1m_AB * E_AB
energy_BA = n1m_BA * E_BA

diff_metric = energy_AA - energy_AB - energy_BA

# --- Select angle range and interpolate ---------------------------------
mask = (angles >= 0.01) & (angles <= 3.0)
angles_f = angles[mask]
energies_f = energies[mask]
diff_f = diff_metric[mask]

interp_angles = np.linspace(angles_f.min(), angles_f.max(), 6000)
interp_energies = interp1d(angles_f, energies_f, kind='linear')(interp_angles)
interp_diff = interp1d(angles_f, diff_f, kind='linear')(interp_angles)

# --- Fit -----------------------------------------------------------------
popt, _ = curve_fit(linear, interp_diff, interp_energies)
a, b = popt
fitted = linear(interp_diff, a, b)

# --- Plot ----------------------------------------------------------------
plt.figure(figsize=(8,6))
plt.plot(interp_angles, interp_energies, label='data', linewidth=2)
plt.plot(interp_angles, fitted, linestyle='--', label=f'fit: a={a:.6e}, b={b:.6e}', linewidth=2)
plt.xlim(0.01, 3.0)
plt.xlabel('Twist angle (deg)')
plt.ylabel('Interlayer energy (meV/atom)')
plt.legend()
plt.tight_layout()
plt.show()

print(f'Fitting parameters: a = {a:.6e}, b = {b:.6e}')

