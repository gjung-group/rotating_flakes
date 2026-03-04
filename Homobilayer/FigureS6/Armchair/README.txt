# README — Hexflake Moiré Analysis Script

## Purpose

This script computes Moiré length and counts registry points (AA, AB, BA) that fall
inside a rotated hexagonal flake for a range of twist angles. It is intended for
producing input data files for a database of flake–substrate interaction / moiré
analyses.

## Files

* `flakeR500.dat` (default output): CSV-like whitespace-separated
  file with one row per twist angle.
* `hexflake_moire.py` (example): the Python script that produced the output.

## Dependencies

* Python 3.8+ (recommended)
* numpy
* matplotlib (only needed if plotting is enabled)

Install dependencies (pip):

```
pip install numpy matplotlib
```

## Script behaviour (summary)

For every twist angle in `theta_values` the script does the following:

1. Computes the Moiré length `L_m` using the lattice constant of hBN, mismatch
   `epsilon`, and the twist angle `theta`.
2. Constructs two basis vectors `a1` and `a2` for the moiré superlattice and
   rotates them by the computed moiré angle.
3. Generates a grid of moiré sites (AA, AB, BA) by integer combinations of the
   rotated basis vectors.
4. Counts how many of these moiré sites lie inside a rotated hexagon of given
   radius (the flake boundary).
5. Writes one line per angle with the results to the output file.

## Key functions

* `calculate_moire_length(a_ref, epsilon, theta_degrees)`
  Computes the moiré length L_m = a_ref / sqrt(epsilon^2 + (1+epsilon)*(2-2*cos(theta))).

* `moire_angle(alpha, theta)`
  Computes the moiré rotation angle (in degrees) from the lattice stretch alpha
  and twist theta. Returns a signed angle in degrees.

* `is_within_hexagon(x, y, radius)`
  Returns True if the point (x, y) lies inside a rotated regular hexagon of the
  specified radius. Uses a point-in-polygon routine.

## Input parameters to edit

Open the script and edit these variables near the top to change behaviour:

* `a_g`  : graphene lattice constant (Å) — default `2.46019`
* `a_hbn`: hBN lattice constant (Å) — default `2.50579`
* `theta_values`: list or numpy range of twist angles (degrees). Default in the
  script is `np.arange(0.0, 5.01, 0.01)`.
* `radius`: flake radius in Å. The example uses `500 * a_g`.
* `output_file_path`: full path to the output file. The script will create the
  directory if it does not exist.

## Output format

Each line in the output file (whitespace-separated) contains the following fields
(written as one formatted string in the script):

1. `Theta (deg)`  — formatted to 3 decimal places
2. `Moire Length (Å)` — formatted to 3 decimal places
3. `AA Count` — integer: number of AA registry points within the flake
4. `AB Count` — integer: number of AB registry points within the flake
5. `BA Count` — integer: number of BA registry points within the flake
6. `Radius (Å)` — flake radius used in the calculation

Example line (fields are padded and separated by spaces):

```
0.000          1393.123              1024                1010                1008                1230.000
```

## Notes and suggestions

* The point-in-polygon routine is a simple ray-casting implementation and is
  sufficient for regular polygons of moderate size. If you need high performance
  or robustness for very large grids, consider using `shapely` for polygon
  operations (`pip install shapely`).

* The current script generates a fixed grid range `m, n in [-55, 54]` for the
  moiré lattice. Change these limits if you need a denser/ larger sample of
  moiré points.

* Commented-out plotting code using `matplotlib` is present. Enable it if you
  want to visualize the point distributions and the hexagon boundary.

## Usage example (command line)

Run the script with Python; it writes the output file to the configured path:

```
python SC.py


