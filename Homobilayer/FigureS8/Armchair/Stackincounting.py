import math
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

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

# Function to check if a point is within a rotated hexagon
def is_within_hexagon(x, y, radius):
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    vertices = np.array([(radius * np.cos(angle), radius * np.sin(angle)) for angle in angles])
    
    rotation_matrix = np.array([[0, 1], [-1, 0]])
    rotated_vertices = np.dot(vertices, rotation_matrix.T)
    rotated_vertices = np.append(rotated_vertices, [rotated_vertices[0]], axis=0)
    
    def point_in_polygon(px, py, poly):
        n = len(poly)
        inside = False
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
            p1x, p1y = p2x, p2y
        return inside
    
    return point_in_polygon(x, y, rotated_vertices)

# # Define lattice constants
a_g = 2.46019  # Graphene lattice constant in angstroms
a_hbn = 2.50579  # hBN lattice constant in angstroms
epsilon = (a_g - a_hbn) / a_hbn
alpha = 1 + epsilon
theta_values = np.arange(6.0, 10.01, 0.01).tolist() 
# theta_values = [4, 5]  # Twist angles in degrees
radius = 500 * a_g  # Define radius

# Output file path
output_file_path = "*******************/Hexflake_GBN_500.dat"
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Writing data to file
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

#     fig, axs = plt.subplots(1, len(theta_values), figsize=(15, 7))
    for idx, theta_degrees in enumerate(theta_values):
        moire_length = calculate_moire_length(a_hbn, epsilon, theta_degrees)
        length_a1 = moire_length
        angle_deg = 60
        angle_rad = np.radians(angle_deg)
    

        
        a1 = np.array([length_a1, 0.0])
        a2 = np.array([length_a1 * np.cos(angle_rad), length_a1 * np.sin(angle_rad)])
        
        moire_angle_deg = moire_angle(alpha, theta_degrees)
        moire_angle_rad = np.radians(moire_angle_deg)
        rotation_matrix = np.array([
            [np.cos(moire_angle_rad), -np.sin(moire_angle_rad)],
            [np.sin(moire_angle_rad),  np.cos(moire_angle_rad)]
        ])
        
        a1_rotated = np.dot(rotation_matrix, a1)
        a2_rotated = np.dot(rotation_matrix, a2)
        
        AAdotsVec, ABdotsVec, BAdotsVec = [], [], []
        for m in range(-100, 100):
            for n in range(-100, 100):
                point_AA = m * a1_rotated + n * a2_rotated
                point_AB = point_AA + (1/3) * a1_rotated + (1/3) * a2_rotated
                point_BA = point_AA + (2/3) * a1_rotated + (2/3) * a2_rotated
                AAdotsVec.append(point_AA)
                ABdotsVec.append(point_AB)
                BAdotsVec.append(point_BA)
        
        points_within_hexagon_AA = sum(is_within_hexagon(point[0], point[1], radius) for point in AAdotsVec)
        points_within_hexagon_AB = sum(is_within_hexagon(point[0], point[1], radius) for point in ABdotsVec)
        points_within_hexagon_BA = sum(is_within_hexagon(point[0], point[1], radius) for point in BAdotsVec)
        
        writer.writerow([
            f"{theta_degrees:<15.3f}"
            f"{moire_length:<23.3f}"
            f"{points_within_hexagon_AA:<20}"
            f"{points_within_hexagon_AB:<20}"
            f"{points_within_hexagon_BA:<20}"
            f"{radius:<10.3f}"
        ])

        angles = np.linspace(0, 2 * np.pi, 7)
        hexagon_x = radius * np.cos(angles)
        hexagon_y = radius * np.sin(angles)
        rotated_hexagon = np.dot(np.vstack((hexagon_x, hexagon_y)).T, np.array([[0, 1], [-1, 0]]).T)

# plt.tight_layout()
# plt.show()
print(f"\nData has been saved to {os.path.abspath(output_file_path)}")
