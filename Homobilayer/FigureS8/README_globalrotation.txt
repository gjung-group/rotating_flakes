# README — Per‑Atom Rotation Angle Calculation Script

This repository contains a clean Python script for computing **per‑atom rotation angles** and the **global best‑fit rotation** between two atomic configurations of a graphene (or other 2D material) flake before and after relaxation.

The script is designed for moiré systems such as **graphene/hBN**, where local rotational variations of the flake are important.

---

##  Purpose of the Script

This script:

1. **Reads two `.xyz` files** — initial and final atomic structures.
2. **Selects only the flake atoms** at a given `z` height (e.g., `z = 19.175 Å`).
3. **Aligns both configurations by their centers of mass**.
4. Computes:

   * **Per‑atom signed rotation angle** (in 2D)
   * **Global best‑fit rotation angle** using SVD
5. **Writes all angles** to a clean text file: `rotation_angles.txt`.
6. Prints useful summaries (min/max angles, sorted angles, filtered angles).

There is **no plotting** in this version — this is a pure analysis script.

---

## File Structure

```
.
├── rotation_angle_script.py     # main script (user names it as needed)
└── README.md                    # this file
```

Data files must be supplied by the user.

---

## Required Input Files

### 1. Initial Configuration (`generateInit.xyz`)

### 2. Relaxed Configuration (`generate.xyz`)

Both must be valid `.xyz` files with the format:

```
<number of atoms>
comment line
Element x y z
Element x y z
...
```

The script skips the first 2 lines and reads only coordinates.

---

## Script Settings

At the top of the script, edit these paths:

```python
INIT_XYZ = "path/to/generateInit.xyz"
FINAL_XYZ = "path/to/generate.xyz"
OUT_TXT  = "path/to/rotation_angles.txt"
Z_FLAKE  = 19.175      # z‑height for selecting flake atoms
ANGLE_FILTER = (-10, 10)  # optional filtering for printed summaries
```

---

## Running the Script

Run from the terminal:

```
python3 rotation_angle_script.py
```

This will:

* read both `.xyz` files
* compute rotation angles
* save them to the output file
* print global rotation and angle summaries

---

## Output File Format

`rotation_angles.txt` contains:

```
# Atom_index  rotation_deg
23 -0.143252
24  0.004521
...
```

*Atom indices correspond to the original `.xyz` ordering.*

---

##  How Rotation is Calculated

### Per‑Atom Rotation

For each atom:

* take initial 2D position (centered)
* take final 2D position (centered)
* compute signed rotation using

```
angle = atan2(det, dot)
```

Mapped into the range **(−180°, 180°]**.

### Global Rotation

Computed using best‑fit 2D rotation matrix from SVD:

```
R = U @ Vᵀ
θ = atan2(R[1,0], R[0,0])
```

This gives the flake‑wide rotation.

---

## Dependencies

Only two packages are required:

```
numpy
matplotlib   # not used in this no‑plot version, can be removed
```

(matplotlib may be removed if desired.)

---

## Notes

* The script assumes a **single flake plane** at constant `z`. Adjust `Z_FLAKE` if needed.
* Works for any 2D material where initial and final `.xyz` files exist.

---


Once you obtain the rotation_angles.txt , then use the generate.xyz and rotation_angles.txt to get the final map using the plot.py







## Contact / Customization

mailid : prathapjharapla@gmail.com

