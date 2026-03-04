import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import MaxNLocator

# === PRL Golden Ratio Setup ===
golden_ratio = (5 ** 0.5 - 1) / 2
fig_width = 7
num_flakes = 9
fig_height = fig_width * golden_ratio * num_flakes / 3.5

# === Data directory ===
data_directory = "/Users/jharaplaprathap/Desktop/FLakes/GBN/Zigzag"

# === Flake sizes and filenames ===
data_filenames = [
    "energy1000.dat", "energy800.dat", "energy700.dat", "energy600.dat",
    "energy500.dat", "energy400.dat", "energy300.dat", "energy200.dat", "energy100.dat"
]
flake_sizes = [1000, 800, 700, 600, 500, 400, 300, 200, 100]

# === Your specified twist angles (one per flake size) ===
twist_angles = [1.25, 1.65, 1.79, 1.85, 1.90, 1.92, 1.94, 1.96, 1.97]  # 100 → 1000

# === Angle range ===
angle_min, angle_max = 1, 2.38

# === Plot Setup ===
fig, axes = plt.subplots(num_flakes, 1, figsize=(fig_width, fig_height), sharex=True, dpi=600)

for i, (filename, flake_size) in enumerate(zip(data_filenames, flake_sizes)):
    filepath = os.path.join(data_directory, filename)
    ax = axes[i]

    if os.path.isfile(filepath):
        data = np.genfromtxt(filepath)
        x = data[:, 0]
        y = data[:, 1]
        y -= np.max(y)

        mask = (x >= angle_min) & (x <= angle_max)
        x_filt, y_filt = x[mask], y[mask]

        if len(x_filt) == 0:
            continue

        new_x = np.linspace(min(x_filt), max(x_filt), num=len(x_filt) + 10000)
        new_y = np.interp(new_x, x_filt, y_filt)
        smooth_y = gaussian_filter1d(new_y, sigma=10)

        # Peaks and valleys
        valleys, _ = find_peaks(-smooth_y, distance=50)
        peaks, _ = find_peaks(smooth_y, distance=50)

        valley_x = new_x[valleys]
        valley_y = smooth_y[valleys]
        peak_x = new_x[peaks]
        peak_y = smooth_y[peaks]

        filtered_valleys = [(x, y) for x, y in zip(valley_x, valley_y) if x not in peak_x]
        filtered_peaks = [(x, y) for x, y in zip(peak_x, peak_y) if x not in valley_x]
        valley_x, valley_y = zip(*filtered_valleys) if filtered_valleys else ([], [])
        peak_x, peak_y = zip(*filtered_peaks) if filtered_peaks else ([], [])

        # === Interpolate energy at specified twist angle ===
        custom_angle = twist_angles[::-1][i]  # reversed to match top-down order
        energy_at_angle = np.interp(custom_angle, new_x, smooth_y)
        print(f"Flake size {flake_size} | Angle {custom_angle:.2f}° → Energy: {energy_at_angle:.6f}")

        # === Main plot ===
        ax.plot(new_x, smooth_y, color='black', linewidth=2.5)
        ax.scatter(valley_x, valley_y, color='blue', s=40, zorder=5)
        ax.scatter(peak_x, peak_y, color='red', s=40, zorder=5)


        # === Axis formatting ===
      

        # Formatting the axes
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.2)
        ax.tick_params(axis='x', which='major', length=12, width=2, labelsize=15)
        ax.tick_params(axis='x', which='minor', length=12, width=2, labelsize=15)
        ax.tick_params(axis='y', which='minor', length=12, width=2, labelsize=15)
        ax.tick_params(axis='y', which='major', length=12, width=2, labelsize=15)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=2))
#         ax.set_xticklabels([])
#         ax.set_yticklabels([])

        # === Draw vertical lines ===
        ax.axvline(1.89, linestyle="dashed", linewidth=4.5, color='orange')  # reference line

        if flake_size != 100:
            ax.spines['bottom'].set_visible(False)  # Hide bottom spine
            ax.set_xticks([])  # Remove x-ticks
          
        else:
            ax.spines['bottom'].set_visible(True)  # Show bottom spine
#          

        for spine in ax.spines.values():
            spine.set_linewidth(2.5)

        ax.spines['bottom'].set_position(('outward', 5))
        ax.set_xlim(angle_min, angle_max)

# === Final adjustments ===
plt.tight_layout(rect=[0, 0, 1.2, 1.4])
plt.subplots_adjust(hspace=0.3)
plt.show()

