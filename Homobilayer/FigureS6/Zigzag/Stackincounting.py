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
    denominator = alpha * np.cos(np.radians(theta)) - 1.0
    moire_angle_rad = np.arctan2(numerator,denominator)  # Use arctan2 for correct quadrant
    moire_angle_deg = np.degrees(moire_angle_rad)
    return moire_angle_deg

# Function to check if a point is within or on the boundary of the hexagon
def is_within_or_on_hexagon(x, y, radius):
    # Define the vertices of the hexagon
    angles = np.linspace(0, 2 * np.pi, 7, endpoint=False)
    vertices = np.array([(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles])
    
    # Add the first vertex to the end to close the hexagon
    vertices = np.append(vertices, [vertices[0]], axis=0)
    
    # Check if the point is within or on the hexagon boundary
    def point_in_polygon(px, py, poly):
        n = len(poly)
        inside = False
        on_boundary = False
        p1x, p1y = poly[0]
        for i in range(n):
            p2x, p2y = poly[i % n]
            if py > min(p1y, p2y):
                if py <= max(p1y, p2y):
                    if px <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (py - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or px <= xinters:
                            inside = not inside
            if (px, py) == (p1x, p1y) or (px, py) == (p2x, p2y):
                on_boundary = True
            p1x, p1y = p2x, p2y
        return inside or on_boundary
    
    return point_in_polygon(x, y, vertices)

# Example usage
a_g = 2.46019  # Graphene lattice constant in angstroms
a_hbn = 2.50579  # hBN lattice constant in angstroms
epsilon = (a_g - a_hbn) / a_hbn

alpha = 1 + epsilon
theta_values = [1.56,1.9] 
# theta_values = np.linspace(0.01, 10, 1001) 
# theta_values = np.arange(0.01, 5.01, 0.01).tolist() 
radius = 100 * a_g # Define radius

# output_file_path = "*************/Hexflakegraphene_GBN_500.dat"

# Plotting section
fig, axs = plt.subplots(1, len(theta_values), figsize=(15, 7),dpi=1000)

for idx, theta_degrees in enumerate(theta_values):
    moire_length = calculate_moire_length(a_hbn, epsilon, theta_degrees)

    length_a1 = moire_length
    angle_deg = 60
    angle_rad = np.radians(angle_deg)

    a1 = np.array([length_a1, 0.0])
    a2 = np.array([length_a1 * np.cos(angle_rad), length_a1 * np.sin(angle_rad)])

    # Rotation matrix for twist angle
    moire_angle_deg = moire_angle(alpha, theta_degrees)
    moire_angle_rad = np.radians(moire_angle_deg)

    rotation_matrix = np.array([
        [np.cos(moire_angle_rad), - np.sin(moire_angle_rad)],
        [np.sin(moire_angle_rad),  np.cos(moire_angle_rad)]
    ])

    # Rotate a1 and a2 using the rotation matrix
    a1_rotated = np.dot(rotation_matrix, a1)
    a2_rotated = np.dot(rotation_matrix, a2)

    # Generate lattice points
    AAdotsVec = []
    ABdotsVec = []
    BAdotsVec = []

    for m in range(-5, 5):
        for n in range(-5,5):
            point_AA = m * a1_rotated + n * a2_rotated
            point_AB = point_AA + (1/3) * a1_rotated + (1/3) * a2_rotated
            point_BA = point_AA + (2/3) * a1_rotated + (2/3) * a2_rotated
            AAdotsVec.append(point_AA)
            ABdotsVec.append(point_AB)
            BAdotsVec.append(point_BA)

    # Count the number of points within the hexagon
    points_within_hexagon_AA = sum(is_within_or_on_hexagon(point[0], point[1], radius) for point in AAdotsVec)
    points_within_hexagon_AB = sum(is_within_or_on_hexagon(point[0], point[1], radius) for point in ABdotsVec)
    points_within_hexagon_BA = sum(is_within_or_on_hexagon(point[0], point[1], radius) for point in BAdotsVec)
    
    # Print results in columns
    print(f"{theta_degrees:<15.3f} | {moire_length:<23.3f} | {points_within_hexagon_AA:<20} | {points_within_hexagon_AB:<20} | {points_within_hexagon_BA:<20}")

    ax = axs[idx]
    ax.scatter([point[0] for point in AAdotsVec], [point[1] for point in AAdotsVec], s=30, label='AA Points', color='black')
    ax.scatter([point[0] for point in ABdotsVec], [point[1] for point in ABdotsVec], s=30, label='AB Points', color='red')
    ax.scatter([point[0] for point in BAdotsVec], [point[1] for point in BAdotsVec], s=30, label='BA Points', color='blue')
    # Define the hexagon
    angles = np.linspace(0, 2 * np.pi, 7)
    hexagon_x = radius * np.cos(angles)
    hexagon_y = radius * np.sin(angles)

    ax.plot(hexagon_x, hexagon_y, 'g-', label='Hexagon Boundary')

    # Set equal scaling
    ax.set_aspect('equal', adjustable='box')

    # Add labels and legend
    ax.set_xlabel('x (Å)')
    ax.set_ylabel('y (Å)')
    ax.set_title(f'Theta = {theta_degrees}°')
#     ax.legend(prop={'size': 10})

# Display the plot
plt.tight_layout()
plt.show()





