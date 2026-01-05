# Day 08 – Band Structure Analysis with adiabatic and non-adiabatic (NA) Electron–Phonon Corrections

This directory contains Python scripts developed as part of **Day 08** of the *Python Course Assignments*. The focus of this exercise is on **analyzing and visualizing electronic band structures** with **NA-electron–phonon (EF)** and **adiabatic corrections**, using data stored in HDF5 (`.h5`) files.

---

## 📁 Directory Contents

```
day08/
├── EF-bandstructure.py   # Main script for band structure plotting
├── utilities.py          # Helper functions for data loading and processing
├── EF_data_demo.py #slicing the real data to samller datasets that are saved in ./data/
├── data/                 # Directory containing .h5 input files (not always included)
└── README.md             # This file
```

---

## 🧠 Overview

The workflow implemented in this folder:

1. **Load electronic structure data** from HDF5 files
2. **Apply energy unit conversion** (Ry → eV)
3. **Construct high-symmetry k-point paths** in the Brillouin zone
4. **Smooth band energies** for visualization
5. **Plot band structures** with:

   * Unperturbed energies
   * NA corrections
   * Adiabatic corrections

Two example systems are included in the main script:

* **MoS₂**
* **Pentacene**

---

## 📜 Scripts Description

### `utilities.py`

A collection of helper functions used throughout the analysis:

* `load_h5_data(path)`
  Loads k-points, occupations, and energy corrections from an HDF5 file.

* `make_kpath(rk, hsp)`
  Builds a continuous k-point path between high-symmetry points.

* `get_smooth(y, n_points=1000)`
  Smooths band energies using cubic spline interpolation.

* Additional helpers for k-point wrapping, path construction, and plotting styles.

---

### `EF-bandstructure.py`

The main executable script that:

* Defines plotting configurations for different materials
* Loads data using `utilities.py`
* Normalizes energies with respect to the Fermi level
* Generates band structure plots with matplotlib

Run the script using:

```bash
python EF-bandstructure.py
```

---

## 📦 Requirements

The scripts require the following Python packages:

* `numpy`
* `matplotlib`
* `h5py`
* `scipy`

You can install them with:

```bash
pip install numpy matplotlib h5py scipy
```

---

## 📊 Output

The script produces **band structure plots** showing:

* Black solid lines: unperturbed bands
* Circles: EF-corrected energies
* Crosses: adiabatic-corrected energies

Vertical lines mark high-symmetry k-points, and the Fermi level is shown as a dashed horizontal line.
