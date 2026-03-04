# Rotating Flakes in Graphene / hBN Systems

This repository contains the input files, data, and analysis scripts used in the study of rotational alignment and energetics of graphene flakes on hexagonal boron nitride (hBN).

The repository accompanies the manuscript:

P. Jharapla et al.,
*Geometric Control of Twist Angle in Moiré Heterobilayer Flakes*
Physical Review B (Year).

---

## Repository Structure

The repository is organized according to the physical systems studied in the work.

```
Hetrobilayer_GBN/
    Input files and analysis scripts for graphene flakes on hBN substrates

Homobilayer/
    Input files and analysis scripts for graphene flakes on graphene substrates
```

Within each directory, subfolders correspond to the different analyses and figures presented in the manuscript.

Typical structure:

```
Figure1/
Figure2/
Figure3/
Figure4/
Figure5/
```

Each figure directory contains the data files and plotting scripts used to generate the corresponding figure.

---

## Large Input Files

Some large input files are stored using **Git Large File Storage (Git LFS)**.

After cloning the repository, run:

```
git lfs install
git lfs pull
```

to download the full data.

---

## Requirements

The plotting and analysis scripts require:

* Python 3
* numpy
* matplotlib

Most scripts can be executed directly with:

```
python script_name.py
```

---

## Reproducing the Figures

Each figure directory contains the data and scripts necessary to reproduce the analysis.

For example:

```
cd Hetrobilayer_GBN/Figure2
python plot.py
```

This will regenerate the corresponding figure using the stored data files.

---

## Citation

If you use this repository or the associated data, please cite:

P. Jharapla et al.,
*Geometric Control of Twist Angle in Moiré Heterobilayer Flakes*,
Physical Review B (Year).

---

## License

This repository is released under the MIT License.

