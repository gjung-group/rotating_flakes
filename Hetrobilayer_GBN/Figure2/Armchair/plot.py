import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.ticker import MaxNLocator

# Publication-quality plotting parameters
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30
plt.rcParams['lines.linewidth'] = 3
plt.rcParams['axes.titlesize'] = 24
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 25
plt.rcParams['ytick.labelsize'] = 25

# Data directory
data_directory = "*************/Path"

# Data files
data_files = {
    "100 Total Energy": "E_inter_energy100.dat",
    "300 Total Energy": "E_inter_energy300.dat",
    "500 Total Energy": "E_inter_energy500.dat",
    "1000 Total Energy": "E_inter_energy1000.dat"
}

# Containers
x_combined = []
y_combined = []
labels = []
first_y_values = {}

# Plot styling
colors = ['black']
line_styles = ['-']

# Angle filter
angle_min, angle_max = 0, 3

# Read and process data
for label, filename in data_files.items():
    file_path = os.path.join(data_directory, filename)

    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        data = np.genfromtxt(file_path)

        if data.ndim == 2 and data.shape[1] >= 2:
            x = data[:, 0]
            y = data[:, 1]

            mask = (x >= angle_min) & (x <= angle_max)
            x_filtered = x[mask]
            y_filtered = y[mask]

            if len(y_filtered) > 0:
                first_y_value = y_filtered[0]
                first_y_values[label] = first_y_value
                print(f"First y-value for dataset {label}: {first_y_value:.5f}")

                x_combined.append(x_filtered)
                y_combined.append(y_filtered - first_y_value)
                labels.append(label)
        else:
            print(f"File {file_path} does not have the expected format.")
    else:
        print(f"File {file_path} does not exist or is empty.")

# Renormalize using the first y-value of 100 Total Energy
if "100 Total Energy" in first_y_values:
    normalization_reference = first_y_values["100 Total Energy"]
    renormalized_y_combined = []

    for i, y_data in enumerate(y_combined):
        dataset_label = labels[i]
        normalization_factor = first_y_values[dataset_label] / normalization_reference
        renormalized_y_combined.append(y_data * normalization_factor)

    # Plot
    fig, axes = plt.subplots(
        len(data_files), 1,
        sharex='col',
        figsize=(10, 12),
        gridspec_kw={'hspace': 0.0001},
        dpi=600
    )

    if len(data_files) == 1:
        axes = [axes]

    for i, ax in enumerate(axes):
        ax.plot(
            x_combined[i],
            renormalized_y_combined[i],
            linestyle=line_styles[0],
            color=colors[0]
        )

        ax.tick_params(axis='both', which='major', length=12, width=2, labelsize=15)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))

        for spine in ax.spines.values():
            spine.set_linewidth(2.5)

        ax.axvline(0.61, linestyle="dashed", linewidth=3, color='red')
        ax.set_xlim(angle_min, angle_max)

    plt.show()

else:
    print("First y-value for 100 Total Energy not found. Renormalization cannot be performed.")

