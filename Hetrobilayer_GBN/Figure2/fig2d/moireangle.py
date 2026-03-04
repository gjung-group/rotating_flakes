import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Function to calculate the moiré angle
def moire_angle(alpha, theta):
    numerator = alpha * np.sin(np.radians(theta))
    denominator = alpha * np.cos(np.radians(theta)) - 1.0   # Avoid division by zero
    moire_angle_rad = np.arctan(numerator / denominator)  # Using arctan for quadrant handling
    moire_angle_deg = np.degrees(moire_angle_rad)
    return moire_angle_deg

# Graphene lattice constant
a_g_values = 2.46019

# hBN lattice constant
base_a_hBN = 2.50579
a_hBN_values = np.array([base_a_hBN * (1.0 + p) for p in np.linspace(-0.01, 0.01, 5, endpoint=True)])
print(a_hBN_values)

# Calculate epsilon and alpha values
# epsilon_values = (a_hBN_values  a_g_values) / a_g_values
epsilon_values = (a_g_values - a_hBN_values ) / a_hBN_values
print(epsilon_values)
alpha_values = 1 + epsilon_values

# Twist angle range
twist_angles = np.linspace(0, 5, 3000)

# Colors for plots
colors = ['b', 'g', 'r', 'c', 'm', 'y']

plt.figure(figsize=(8, 6), dpi=300)

# Plot for α = 1 (dashed line)
moire_angles_1 = [moire_angle(1, theta) + 60 for theta in twist_angles]
plt.plot(twist_angles, moire_angles_1, 'k--', label='α = 1', linewidth=2,color='magenta')

# Plot for other α values (solid lines)
for i, alpha in enumerate(alpha_values):
    moire_angles = [moire_angle(alpha, theta) for theta in twist_angles]
    plt.plot(twist_angles, moire_angles, label=f'α = {alpha:.4f}', linewidth=2, color=colors[i % len(colors)])

# Find the angles closest to 30° and 60°
closest_30 = {}
closest_60 = {}
for alpha in alpha_values:
    moire_angles = np.array([moire_angle(alpha, theta) for theta in twist_angles])
    idx_30 = np.abs(moire_angles + 30).argmin()
    idx_60 = np.abs(moire_angles + 60).argmin()
    closest_30[alpha] = twist_angles[idx_30]
    closest_60[alpha] = twist_angles[idx_60]

print(f"{'Alpha':<12} {'epsilon_values':<18} {'Theta (near 30°)':<22} {'Theta (near 60°)':<22}")
for eps, alpha in zip(epsilon_values, alpha_values):
    print(f"{alpha:<12.6f} {eps:<18.6f} {closest_30[alpha]:<22.6f} {closest_60[alpha]:<22.6f}")

# Highlight the closest points on the plot
first_alpha = alpha_values[0]
for alpha in alpha_values:
    plt.scatter(closest_30[alpha], -30, color='cornflowerblue', marker='o', s=100,
                label=r'$\theta$ near $30^\circ$' if alpha == first_alpha else "")
    plt.scatter(closest_60[alpha], -60, color='lightcoral', marker='*', s=130,
                label=r'$\theta$ near $60^\circ$' if alpha == first_alpha else "")

plt.axhline(-30, linestyle="dotted", linewidth=3, color='black', label=r'$30^\circ$')
plt.axhline(-60, linestyle="dotted", linewidth=3, color='dimgrey', label=r'$60^\circ$')
plt.xlim(0, 5)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Adjust tick format
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(15))

# Customize figure borders
plt.gca().tick_params(axis='both', which='major', length=12, width=2)
plt.gca().spines['top'].set_linewidth(1.5)
plt.gca().spines['right'].set_linewidth(1.5)
plt.gca().spines['bottom'].set_linewidth(1.5)
plt.gca().spines['left'].set_linewidth(1.5)
# plt.gca().set_xticklabels([]) 
# plt.gca().set_yticklabels([])
plt.xlabel('Twist Angle (degrees)', fontsize=24)
plt.ylabel('Moiré Angle (degrees)', fontsize=24)
# plt.legend()
plt.show()

