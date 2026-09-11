# FTMC BSA–PEF Molecular Dynamics Project

## Overview
This repository contains the computational work performed during my internship at the Center for Physical Sciences and Technology (FTMC), Vilnius.

The project focuses on investigating how external electric fields may influence the structure and dynamics of bovine serum albumin (BSA), with the longer-term goal of comparing computational results with experimental observations available from the research group.

## Internship
- Student: Ahmed Yomi Isiaka
- Programme: MSc Systems Biology, Vilnius University
- Host: Center for Physical Sciences and Technology (FTMC)
- Supervisor: Dr. Arūnas Stirkė
- Internship period: 16 September 2026 – 16 November 2026

## Initial model protein
- Protein: Bovine serum albumin (BSA)
- Gene: ALB
- Organism: Bos taurus
- UniProt accession: P02769
- Mature chain: UniProt residues 25–607
- Mature protein length: 583 amino acids
- Initial candidate structure: PDB 4F5S
- Experimental method: X-ray diffraction
- Resolution: 2.47 Å

## Project objectives
1. Review published evidence on electric-field effects on proteins.
2. Characterize BSA sequence and structural features.
3. Select and prepare a suitable experimental BSA structure.
4. Establish a baseline molecular-dynamics simulation without an electric field.
5. Analyse structural properties such as RMSD, RMSF, radius of gyration, solvent-accessible surface area, hydrogen bonding and secondary structure.
6. Investigate selected electric-field conditions after the control workflow has been validated.
7. Compare computational trends with relevant experimental observations from the FTMC group where possible.

## Repository structure

```text
docs/                       Research notes and documentation
data/raw/                   Original input structures and source files
data/processed/             Cleaned or processed structural files
scripts/                    Analysis and preprocessing scripts
analysis/                   Analysis outputs and intermediate results
figures/                    Final figures
simulations/control/        Baseline molecular-dynamics simulation
simulations/electric_field/ Electric-field simulations
