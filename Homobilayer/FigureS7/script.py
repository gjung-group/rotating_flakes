
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.ticker import MaxNLocator

# Set publication quality parameters
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 30
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.labelsize'] = 20
plt.rcParams['xtick.labelsize'] = 25
plt.rcParams['ytick.labelsize'] = 25

# Specify the directory and filenames for rigid and relaxed data
data_directory = "***********************"
rigid_filename = "E_inter_energy500_Rigid.dat"
relaxed_filename = "E_inter_energy500_Relaxed.dat"

# Define the angle filter ranges for individual plots
angle_ranges = [(1.5, 2.5)]

# Define separate shift values for rigid and relaxed datasets
shift_rigid =   -19.264610
shift_relaxed =  -19.645346 #-20.700337 #-19.264608 #-20.700337

# Function to process data file
def load_and_process_data(file_path, angle_min, angle_max, shift_value):
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        data = np.genfromtxt(file_path)
        if data.ndim == 2 and data.shape[1] >= 2:  # Check data format
            x = data[:, 0]  # Twist Angle values
            y = data[:, 1]  # Energy Data values
            
            # Apply angle range filter
            filter_mask = (x >= angle_min) & (x <= angle_max)
            x_filtered = x[filter_mask]
            y_filtered = y[filter_mask]
            
            # Normalize using specified shift value
            y_filtered -= shift_value
            
            # Interpolate data for smooth plot
            interp_func = interp1d(x_filtered, y_filtered, kind='cubic')
            x_interp = np.linspace(np.min(x_filtered), np.max(x_filtered), 1000)
            y_interp = interp_func(x_interp)
            
            return x_interp, y_interp
    else:
        print(f"File {file_path} does not exist or is empty.")
    return None, None

# Colors and line styles for rigid and relaxed data
colors = ['black', 'red']
labels = ['Rigid Data', 'Relaxed Data']

# Create individual plots for each angle range
for i, (angle_min, angle_max) in enumerate(angle_ranges):
    # Load rigid data with its specific shift value
    rigid_path = os.path.join(data_directory, rigid_filename)
    x_rigid_interp, y_rigid_interp = load_and_process_data(rigid_path, angle_min, angle_max, shift_rigid)
    
    # Load relaxed data with its specific shift value
    relaxed_path = os.path.join(data_directory, relaxed_filename)
    x_relaxed_interp, y_relaxed_interp = load_and_process_data(relaxed_path, angle_min, angle_max, shift_relaxed)
    
    # Create a new figure for each plot
    fig, ax = plt.subplots(figsize=(10, 6), dpi=700)
    
    # Plot rigid data
    if x_rigid_interp is not None and y_rigid_interp is not None:
        ax.plot(x_rigid_interp, y_rigid_interp, color=colors[0], label=labels[0], linestyle='-', linewidth=3)
    
    # Plot relaxed data
    if x_relaxed_interp is not None and y_relaxed_interp is not None:
        ax.plot(x_relaxed_interp, y_relaxed_interp, color=colors[1], label=labels[1], linestyle='-', linewidth=3)
    
    # Customize the plot
    ax.set_xlim(angle_min, angle_max)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.tick_params(axis='both', which='major', length=12, width=2)
#     ax.set_xticklabels([]) 
#     ax.set_yticklabels([])
    ax.axvline(1.89, linestyle="dashed", linewidth=3, color='blue')
#     ax.grid(True, linestyle='--', linewidth=1, alpha=0.6)

    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
    
    # Save or display each figure
    plt.tight_layout()
    plt.show()

