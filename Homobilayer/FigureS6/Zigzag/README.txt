# README — Moiré Energy Fit Script

This repository contains a  Python script (`ploting.py`) used to
compute and visualize the relationship between twist‐angle–dependent moiré
interlayer energies and a derived domain‑energy. The workflow is designed
for systems such as graphene/hBN zigzag or armchair flakes.

Stackingcounting.py generates the Moire domain count file Zigzag_GBN
---

## 📌 Purpose of the Script

The script:

1. **Loads two data files**:

   * *Angle vs energy file* (`E_inter_energy*.dat`)
   * *Moiré domain‑count file* (`Zigzag_GBN.dat`)
2. **Computes per-domain contributions** (AA, AB, BA) using:

   * Domain counts
   * Moiré cell area
   * Energies per atom (AA, AB, BA)

3. **Forms a metric**:
   `diff_metric = E_AA - E_AB - E_BA`

4. **Interpolates data** for smooth visualization.

5. **Fits a linear relation** between interlayer energy and the computed metric.

6. **Produces a plot** of the data and the fitted line.

This is primarily used to understand energetic alignment trends in moiré
superlattices.

---

## 📂 File Structure

```
.
├── moire_fit.py         # Main script
└── README.md            # This file
```

You must provide your own data files.

---

## 📥 Input Files

### 1. Energy File (e.g., `E_inter_energy.dat`)

Two columns:

1. Angle (degrees)
2. Interlayer energy (meV/atom)

### 2. Domain Count File (e.g., `Zigzag_GBN.dat`)

Expected columns:

```
...,  moire_length,  n_AA,  n_AB,  n_BA,  ...
```

Only columns 2–5 are used.

---

## ▶️ How to Run

Edit the file paths inside the script:

```python
ENERGY_FILE = '/path/to/E_inter_energy.dat'
AB_FILE     = '/path/to/Zigzag_GBN_.dat'
```

Then run:

```
python3 moire_fit.py
```

A plot window will appear showing:

* Raw interlayer energy vs angle
* Linear fit to the computed metric

The terminal will print:

```
Fitting parameters: a = <value>, b = <value>
```

---

## Output

The script displays a high‑resolution figure of:

* Interpolated energy curve
* Fitted linear relation

Use screenshots or matplotlib's `savefig()` if you want to store the figure.

---

## Dependencies

Install the required packages:

```
pip install numpy matplotlib scipy
```

---

## ✏️ Modifying the Script

You can easily adjust:

* Energy constants: `E_AA`, `E_AB`, `E_BA`
* Radius `R`
* Angle filtering range
* Output plot style

---



