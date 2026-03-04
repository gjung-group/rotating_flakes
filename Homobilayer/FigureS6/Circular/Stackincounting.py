import math
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate Moiré length
def calculate_moire_length(a_ref, epsilon, theta_degrees):
    theta_radians = math.radians(theta_degrees)
    term1 = epsilon ** 2
    term2 = (1 + epsilon) * (2 - 2 * math.cos(theta_radians))
    moire_length = a_ref / math.sqrt(term1 + term2)
    return moire_length

# Function to calculate Moiré angle
def moire_angle(alpha, theta):
    numerator = alpha * np.sin(np.radians(theta))
    denominator = alpha * np.cos(np.radians(theta)) - 1
    moire_angle_rad = np.arctan(numerator/denominator)  # Use arctan2 for correct quadrant
    moire_angle_deg = np.degrees(moire_angle_rad)
    return moire_angle_deg

# Function to check if a point is within or on the boundary of a circle
def is_within_or_on_circle(x, y, radius):
    distance_squared = x**2 + y**2
    return distance_squared <= radius**2

# Example usage
a_g = 2.46019  # Graphene lattice constant in angstroms
a_hbn = 2.50579  # hBN lattice constant in angstroms
epsilon = (a_g - a_hbn) / a_hbn  # Strain (epsilon)
alpha = 1 + epsilon
theta_values = [1.56, 1.90]  # Twist angles in degrees
radius = 100   # Define radius

# Plotting section
fig, axs = plt.subplots(1, len(theta_values), figsize=(15, 7))

for idx, theta_degrees in enumerate(theta_values):
    moire_length = calculate_moire_length(a_g, epsilon, theta_degrees)

    length_a1 = moire_length
    angle_deg = -60
    angle_rad = np.radians(angle_deg)

    a1 = np.array([length_a1, 0.0])
    a2 = np.array([length_a1 * np.cos(angle_rad), length_a1 * np.sin(angle_rad)])

    # Rotation matrix for twist angle
    moire_angle_deg = moire_angle(alpha, theta_degrees)
    moire_angle_rad = np.radians(moire_angle_deg)

    rotation_matrix = np.array([
        [np.cos(moire_angle_rad), -np.sin(moire_angle_rad)],
        [np.sin(moire_angle_rad),  np.cos(moire_angle_rad)]
    ])

    # Rotate a1 and a2 using the rotation matrix
    a1_rotated = np.dot(rotation_matrix, a1)
    a2_rotated = np.dot(rotation_matrix, a2)

    # Generate lattice points
    AAdotsVec = []
    ABdotsVec = []
    BAdotsVec = []

    for m in range(-3,3):
        for n in range(-3, 3):
            point_AA = m * a1_rotated + n * a2_rotated
            point_AB = point_AA + (1/3) * a1_rotated + (1/3) * a2_rotated
            point_BA = point_AA + (2/3) * a1_rotated + (2/3) * a2_rotated
            AAdotsVec.append(point_AA)
            ABdotsVec.append(point_AB)
            BAdotsVec.append(point_BA)

    # Count the number of points within the circle
    points_within_circle_AA = sum(is_within_or_on_circle(point[0], point[1], radius) for point in AAdotsVec)
    points_within_circle_AB = sum(is_within_or_on_circle(point[0], point[1], radius) for point in ABdotsVec)
    points_within_circle_BA = sum(is_within_or_on_circle(point[0], point[1], radius) for point in BAdotsVec)

    # Print results in columns
    print(f"{theta_degrees:<15.3f} | {moire_length:<23.3f} | {points_within_circle_AA:<20} | {points_within_circle_AB:<20} | {points_within_circle_BA:<20}")

    ax = axs[idx]
    ax.scatter([point[0] for point in AAdotsVec], [point[1] for point in AAdotsVec], s=100, label='AA Points', color='black')
    ax.scatter([point[0] for point in ABdotsVec], [point[1] for point in ABdotsVec], s=100, label='AB Points', color='red')
    ax.scatter([point[0] for point in BAdotsVec], [point[1] for point in BAdotsVec], s=100, label='BA Points', color='blue')

    # Define the circle
    circle = plt.Circle((0, 0), radius, color='green', fill=False, label='Circle Boundary')
    ax.add_artist(circle)

    # Set equal scaling
    ax.set_aspect('equal', adjustable='box')

    # Add labels and legend
    ax.set_xlabel('x (\u00c5)')
    ax.set_ylabel('y (\u00c5)')
    ax.set_title(f'Theta = {theta_degrees}°')
    ax.legend(prop={'size': 10})

# Display the plot
plt.tight_layout()
plt.show()

