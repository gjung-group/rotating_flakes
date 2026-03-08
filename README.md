# Rotating Flakes in Graphene / hBN Systems

[![DOI](https://zenodo.org/badge/1144689518.svg)](https://doi.org/10.5281/zenodo.18914172)

The repository is organized into two main folders. Each folder further contains subdirectories corresponding to two edge types: Armchair and Zigzag.

Heterobilayer – Contains data and input files for graphene–hBN systems used to generate the figures in the manuscript.

Homobilayer – Contains data and input files for graphene–graphene, hBN-hBN systems used in the analysis (Supplementary).

Each folder is further organized according to the figures presented in the manuscript.

Prathap Kumar Jharapla, Nicolas Leconte, Zhiren He, Guru Khalsa, and Jeil Jung,
Geometric Control of Twist Angle in Moiré Heterobilayer Flakes,
arXiv:2510.18694 (2025).
https://arxiv.org/abs/2510.18694

---

## Repository Structure

The repository is organized according to the physical systems studied in the work.

```
Heterobilayer/
    Input files and analysis scripts for graphene flakes on hBN substrates

Homobilayer/
    Input files and analysis scripts for graphene flakes on graphene substrates
```

Within each directory, subfolders correspond to the different analyses and figures presented in the manuscript. Each figure folder further contains two sections corresponding to the edge types: Armchair and Zigzag

Typical structure: Heterobilayer

```
Figure1/
Figure2/
Figure3/
Figure4/
Figure5/
```
Typical structure: Homobilayer
```
FigureS1/
FigureS2/
FigureS3/
FigureS4/
FigureS5/
FigureS6/
FigureS7/
FigureS8/
FigureS9/
FigureS10/
FigureS11/
```

Each figure directory contains the data files and plotting scripts used to generate the corresponding figure.

---

## Large Input Files

Some large input files are stored using **Git Large File Storage (Git LFS)**.

In both the Heterobilayer and Homobilayer directories, there are subfolders corresponding to simulations of flakes with a size of 50 Å, with twist angles ranging from θ = 0° to 10°. These folders contain the structural file BLBLNew.mol along with the corresponding LAMMPS input files required to run the simulations.

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
cd Heterobilayer_GBN/Figure2/Armchair
python plot.py
```

This will regenerate the corresponding figure using the stored data files.

---

## Citation

If you use this repository or the associated data, please cite:

P.K.Jharapla et al.,
*Geometric Control of Twist Angle in Moiré Heterobilayer Flakes*,
arXiv:2510.18694 (2025).
https://arxiv.org/abs/2510.18694

---

## License

This repository is released under the MIT License.

