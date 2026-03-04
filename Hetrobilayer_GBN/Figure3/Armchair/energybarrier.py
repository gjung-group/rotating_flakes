import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# -------- Input / Output --------
file_path = "**************/energy100.dat"
output_file = "energy_D100.dat"

# -------- Read data --------
x_vals = []
y_vals = []

with open(file_path, "r") as f:
    for line in f:
        cols = line.split()
        if len(cols) >= 2:
            x_vals.append(float(cols[0]))
            y_vals.append(float(cols[1]))

x_vals = np.array(x_vals)
y_vals = np.array(y_vals)

# -------- Interpolation --------
new_x = np.linspace(x_vals.min(), x_vals.max(), len(x_vals) + 10000)
new_y = np.interp(new_x, x_vals, y_vals)

# -------- Find peaks & valleys --------
peaks, _ = find_peaks(new_y)
valleys, _ = find_peaks(-new_y)

peak_x = new_x[peaks]
peak_y = new_y[peaks]
valley_x = new_x[valleys]
valley_y = new_y[valleys]

# -------- Plot --------
plt.figure(figsize=(10, 6))
plt.plot(new_x, new_y, '-', color='orange', label='Interpolated')
plt.plot(peak_x, peak_y, 'o', color='red', label='Peaks')
plt.plot(valley_x, valley_y, 'o', color='blue', label='Valleys')
plt.xlabel("Twist Angle (°)")
plt.ylabel("Total Energy (eV)")
plt.xlim(0, 7)
plt.legend()
plt.title("Peaks and Valleys")
plt.show()

# -------- Compute alternating energy barriers --------
barriers = []
n = min(len(peak_y), len(valley_y))

for i in range(n):
    barriers.append(peak_y[i] - valley_y[i])
    if i + 1 < len(valley_y):
        barriers.append(valley_y[i + 1] - peak_y[i])

barriers = np.array(barriers)

# -------- Save barriers --------
np.savetxt(output_file, barriers, fmt="%.6f")

# -------- Print summary --------
print("Energy barriers:")
for b in barriers:
    print(b)

max_point = peak_y.max() if len(peak_y) else new_y.max()
min_point = valley_y.min() if len(valley_y) else new_y.min()
barrier_height = max_point - min_point

print(f"\nMaximum Energy: {max_point} eV")
print(f"Minimum Energy: {min_point} eV")
print(f"Barrier Height: {barrier_height} eV")
print(f"\nSaved to {output_file}")

