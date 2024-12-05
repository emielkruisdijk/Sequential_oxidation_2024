# Sequential_oxidation_2024

This folder contains the PHREEQC scripts, python scripts, and data files needed for simulation of the water quality changes in the rapid sand filters.

# Data files:
WQ_data.csv - Contains height profiles of waterquality parameters taken from the pilot-scale rapid sand filters
O2_data.csv - Contains height profiles of dissolved oxygen taken from the pilot-scale rapid sand filters

# Phreeqc models:
wateq4f_updated v3.dat - Database needed for running the phreeqc scripts of the pilot-scale rapid sand filters
AER8.phr - PHREEQC script which was used to simulate pilot-scale filter AER8
LIM6.8-1.phr - PHREEQC script which was used to simulate pilot-scale filter LIM6.8-1
LIM6.8-2.phr - PHREEQC script which was used to simulate pilot-scale filter LIM6.8-2
LIM8-1.phr - PHREEQC script which was used to simulate pilot-scale filter LIM8-1
LIM8-2.phr - PHREEQC script which was used to simulate pilot-scale filter LIM8-2

# Python scripts:
AER8.py - Python script to visualize observed and simulated water quality changes observed in pilot-scale filter AER8
Lim6.8.py - Python script to visualize observed and simulated water quality changes observed in pilot-scale filter LIM6.8
Lim8.py - Python script to visualize observed and simulated water quality changes observed in pilot-scale filter LIM8
Lim6.8-1_nitrite_dependent_MnOx_reduction.py - Python script to visualize the nitrite dependent MnOx reduction observed in pilot-scale filter LIM6.8

# How to use:
Step 1: Run the phreeqc script of the pilot-scale filter you are interested in. The output of the PHREEQC script will be a text file with the simulated concentrations in the pilot-scale rapid sand filter. Make sure that the database file is in the same folder as the PHREEQC model.
Step 2: Run the related python script. The python script uses the data from the phreeqc model and the data files, and will use this data to plot a figure. Make sure that the phreeqc text file and the datafiles are in the same folder as the python script. The python script will give a figure as output.

# Software used
PHREEQC: The PHREEQC plugin for Notepad++ was used to run the PHREEQC scripts (https://hydrochemistry.eu/ph3/index.html). PHREEQC version 3.8.
Python: Python scripts were ran in Spyder in Python 3.12. The following packages were used:
    Matplotlib 3.8.4
    Pandas 2.2.2
