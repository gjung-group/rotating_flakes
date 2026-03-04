import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as mticker

# Define the fitting function
def fit_func(x, a, b):
    return a * x + b

# Constants
R = 500 * 2.46019  # Radius in Ångstroms
E_AA = -18  # Energy per atom for AA (in meV)
E_AB = -19  # Energy per atom for AB (in meV)
E_BA = -23  # Energy per atom for BA (in meV)

# Load the data
data = np.genfromtxt('/Users/jharaplaprathap/Desktop/FLakes/Circularflake/GBN/CGCM/E_inter_energy500.dat')
angles = data[:, 0]
energies = data[:, 1]

data_ab = np.genfromtxt('/Users/jharaplaprathap/Desktop/FLakes/Circularflake/GBN/CGCM/circularflake_GBN_500.dat')


# Define the area of the circle
def area_of_circle(radius):
    return np.pi * radius**2

def area_of_the_cell(moire_length):
    root3 = np.sqrt(3)
    return (root3 / 2) * moire_length**2

def calculate_n1m(num_points, moire_length, AmL, AmR):
    return num_points * (AmL / AmR)

# Calculate areas
AmR = area_of_circle(R)
                        
                        
# Initialize lists to hold data
moire_lengths = data_ab[:, 1]
num_AA_points = data_ab[:, 2]
num_AB_points = data_ab[:, 3]
num_BA_points = data_ab[:, 4]

# Calculate N1M and energies for AA, AB, and BA
n1m_aa, n1m_ab, n1m_ba = [], [], []
energy_aa_list, energy_ab_list, energy_ba_list = [], [], []

for aa, ab, ba, ml in zip(num_AA_points, num_AB_points, num_BA_points, moire_lengths):
    AmL = area_of_the_cell(ml)
    n1m_aa_val = calculate_n1m(aa, ml, AmL, AmR)
    n1m_ab_val = calculate_n1m(ab, ml, AmL, AmR)
    n1m_ba_val = calculate_n1m(ba, ml, AmL, AmR)

    energy_aa = n1m_aa_val * E_AA
    energy_ab = n1m_ab_val * E_AB
    energy_ba = n1m_ba_val * E_BA

    n1m_aa.append(n1m_aa_val)
    n1m_ab.append(n1m_ab_val)
    n1m_ba.append(n1m_ba_val)
    energy_aa_list.append(energy_aa)
    energy_ab_list.append(energy_ab)
    energy_ba_list.append(energy_ba)

# Calculate the energy difference (AA - AB - BA)
diff_AA_AB = np.array(energy_aa_list) - np.array(energy_ab_list) - np.array(energy_ba_list)

# Filter data within the desired range of angles
filter1 = (angles >= 0) & (angles <= 5)
angles_filtered = angles[filter1]
energies_filtered = energies[filter1]
diff_AA_AB_filtered = diff_AA_AB[filter1]

# Interpolate data
interp_angles = np.linspace(np.min(angles_filtered), np.max(angles_filtered), 6000)
interp_energies = interp1d(angles_filtered, energies_filtered, kind='linear', fill_value='extrapolate')(interp_angles)
interp_diff_AA_AB = interp1d(angles_filtered, diff_AA_AB_filtered, kind='linear', fill_value='extrapolate')(interp_angles)

# Perform curve fitting
popt, pcov = curve_fit(fit_func, interp_diff_AA_AB, interp_energies)

# Get the fitting parameters a and b
a, b = popt

# Generate fitted values for the plot
fitted_energies = fit_func(interp_diff_AA_AB, a, b)

# Create a publication-quality figure
fig, ax = plt.subplots(figsize=(8, 6), dpi=700)

# Plot the original data and fitted curve
ax.plot(interp_angles, interp_energies, color='black', linestyle='-', linewidth=3)
ax.plot(interp_angles, fitted_energies, color='red', linestyle='-', linewidth=3)
# Customize labels, title, and legend
ax.set_xlim(0.1, 5)
ax.tick_params(axis='both', which='major', length=12, width=2, labelsize=32)
ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
# ax.set_xticklabels([])
# ax.set_yticklabels([])
# Customize plot spines
for spine in ax.spines.values():
    spine.set_linewidth(2.5)

plt.tight_layout()
plt.xticks(fontname="Times New Roman")
plt.yticks(fontname="Times New Roman")
# plt.legend(fontsize=12)
plt.show()

# Print the fitting parameters
print(f"Fitting parameters: a = {a:.6f}, b = {b:.6f}")

