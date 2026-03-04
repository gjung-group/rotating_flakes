#!/usr/bin/env python3
import numpy as np

# ---------- User-editable paths & settings ----------
INIT_XYZ = "**********************/generateInit.xyz"
FINAL_XYZ = "*********************/generate.xyz"
OUT_TXT  = "**********************/rotation_angles.txt"
Z_FLAKE  = 19.175
ANGLE_FILTER = (-10.0, 10.0)   # used only for printed summaries
# ---------------------------------------------------

def read_xyz_pos(filepath, header_lines=2):
    pos = []
    with open(filepath, "r") as f:
        lines = f.readlines()[header_lines:]
    for L in lines:
        parts = L.split()
        if len(parts) >= 4:
            _, x, y, z = parts[:4]
            pos.append([float(x), float(y), float(z)])
    return np.asarray(pos)

def center_of_mass(pts):
    return np.mean(pts, axis=0)

def signed_angles_2d(v_before, v_after):
    # v_before, v_after: (N,2)
    norm_b = np.linalg.norm(v_before, axis=1, keepdims=True)
    norm_a = np.linalg.norm(v_after,  axis=1, keepdims=True)
    safe = (norm_b.squeeze() > 0) & (norm_a.squeeze() > 0)
    angles = np.zeros(v_before.shape[0], dtype=float)
    if np.any(safe):
        b = v_before[safe] / norm_b[safe]
        a = v_after[safe]  / norm_a[safe]
        det = b[:,0]*a[:,1] - b[:,1]*a[:,0]
        dot = b[:,0]*a[:,0] + b[:,1]*a[:,1]
        ang = np.degrees(np.arctan2(det, dot))
        angles[safe] = (ang + 180) % 360 - 180
    return angles

def global_rotation_angle(bef, aft):
    H = bef.T @ aft
    U, _, Vt = np.linalg.svd(H)
    Rm = U @ Vt
    angle_rad = np.arctan2(Rm[1,0], Rm[0,0])
    return np.degrees(angle_rad)

def main():
    init = read_xyz_pos(INIT_XYZ)
    final = read_xyz_pos(FINAL_XYZ)

    mask = np.isclose(init[:,2], Z_FLAKE)
    idx = np.where(mask)[0]
    if idx.size == 0:
        raise RuntimeError("No flake atoms found at specified z")

    b2 = init[mask, :2].astype(float)
    a2 = final[mask, :2].astype(float)

    cb = center_of_mass(b2)
    ca = center_of_mass(a2)
    b2c = b2 - cb
    a2c = a2 - ca

    angles = signed_angles_2d(b2c, a2c)

    # save results
    with open(OUT_TXT, "w") as f:
        f.write("# Atom_index  rotation_deg\n")
        for i, ang in zip(idx, angles):
            f.write(f"{i} {ang:.6f}\n")
    print(f"Wrote angles to: {OUT_TXT}")

    glob_ang = global_rotation_angle(b2c, a2c)
    print(f"Global rotation (best-fit): {glob_ang:.6f} deg")

    # summaries
    print("All:  min={:.6f}, max={:.6f}".format(angles.min(), angles.max()))
    sorted_angles = np.sort(angles)
    print("5 smallest:", ["{:.6f}".format(a) for a in sorted_angles[:5]])
    print("5 largest :", ["{:.6f}".format(a) for a in sorted_angles[-5:]])

    # optional filtered summary using ANGLE_FILTER
    lo, hi = ANGLE_FILTER
    filt = angles[(angles >= lo) & (angles <= hi)]
    if filt.size:
        print("Filtered ({} to {} deg): min={:.6f}, max={:.6f}, mean={:.6f}".format(
            lo, hi, filt.min(), filt.max(), filt.mean()))
    else:
        print("No angles within filter range.")

if __name__ == "__main__":
    main()

