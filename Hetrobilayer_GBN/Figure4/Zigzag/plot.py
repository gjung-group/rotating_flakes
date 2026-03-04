import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.ticker import MaxNLocator

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 25
plt.rcParams['ytick.labelsize'] = 25

data_directory = "******************************/500/AB"
aa_rigid_file = "E_inter_energy500AA_Rigid.dat"
aa_relaxed_file = "E_inter_energy500AA_Relaxed.dat"  # make sure exists
ab_rigid_file = "E_inter_energy500AB_Rigid.dat"
ab_relaxed_file = "E_inter_energy500AB_Relaxed.dat"

angle_min, angle_max = 1.5, 2.5

shift_values = {
    "AA_Rigid":  -19.306594,
    "AA_Relaxed":  -19.707877,
    "AB_Rigid":  -19.306594,     # adjust if different
    "AB_Relaxed":  -19.707877   # adjust if different
}

# Function to load and process data with high-density interpolation
def load_and_process_data(file_path, angle_min, angle_max, shift_value):
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        data = np.genfromtxt(file_path)
        if data.ndim == 2 and data.shape[1] >= 2:
            x, y = data[:, 0], data[:, 1]
            mask = (x >= angle_min) & (x <= angle_max)
            x, y = x[mask], y[mask]
            y -= shift_value
            interp_func = interp1d(x, y, kind='linear')
            x_interp = np.linspace(np.min(x), np.max(x), 10000)  # smoother curve
            y_interp = interp_func(x_interp)
            return x_interp, y_interp
    print(f"File {file_path} does not exist or is empty.")
    return None, None

# (label, filename, shift_key, color, linestyle, linewidth)
datasets = [
    ("AA Rigid", aa_rigid_file, "AA_Rigid", "black", "--", 1.5),
    ("AA Relaxed", aa_relaxed_file, "AA_Relaxed", "black", "-", 3),
    ("AB Rigid", ab_rigid_file, "AB_Rigid", "red", "--", 1.5),
    ("AB Relaxed", ab_relaxed_file, "AB_Relaxed", "red", "-", 3)
]

fig, ax = plt.subplots(figsize=(10, 6), dpi=700)

for label, filename, shift_key, color, linestyle, lw in datasets:
    file_path = os.path.join(data_directory, filename)
    x_interp, y_interp = load_and_process_data(file_path, angle_min, angle_max, shift_values[shift_key])
    if x_interp is not None:
        ax.plot(x_interp, y_interp, label=label, color=color, linestyle=linestyle, linewidth=lw)

ax.set_xlim(angle_min, angle_max)
ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
ax.tick_params(axis='both', which='major', length=12, width=2)
ax.axvline(1.89, linestyle="dashed", linewidth=3, color='blue')
ax.grid(True, linestyle='--', linewidth=1, alpha=0.6)
# ax.set_xticklabels([]) 
# ax.set_yticklabels([])
for spine in ax.spines.values():
    spine.set_linewidth(2.5)

# plt.ylim(-0.04, 0.02)  # uncomment if needed
# plt.legend(fontsize=18)
plt.tight_layout()
plt.show()

