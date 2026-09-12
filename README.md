# FTMC BSA–PEF Molecular Dynamics Project

## Computational Investigation of Pulsed Electric Field Effects on Bovine Serum Albumin

This repository contains the computational workflow developed during my internship at the **Center for Physical Sciences and Technology (FTMC), Vilnius, Lithuania**.

The project investigates the structural response of **bovine serum albumin (BSA)** to **pulsed electric field (PEF)** exposure, with particular interest in nanosecond pulsed electric fields (nsPEF).

The computational component is designed to complement experimental observations by using molecular dynamics (MD) simulations and structural analyses to investigate how electric fields may influence BSA conformation, stability, dynamics, and intermolecularly relevant structural properties.

---

## Project Aim

The main research question is:

> **How does pulsed electric field exposure affect the structure and conformational dynamics of bovine serum albumin, and can molecular dynamics simulations help explain experimental observations?**

The project combines:

- literature analysis,
- protein sequence and structure preparation,
- molecular dynamics simulations,
- electric-field simulations,
- structural trajectory analysis,
- and comparison with experimentally observed PEF-induced changes.

The MD simulations are not intended to assume a direct numerical equivalence between experimental PEF conditions and molecular-scale electric fields. Experimental and simulation field strengths, exposure times, and physical scales will therefore be interpreted carefully.

---

## Protein System

| Property | Information |
|---|---|
| Protein | Bovine serum albumin |
| Abbreviation | BSA |
| Gene | ALB |
| Organism | *Bos taurus* |
| UniProt accession | P02769 |
| UniProt entry | ALBU_BOVIN |
| Full precursor length | 607 amino acids |
| Signal peptide | Residues 1–18 |
| Propeptide | Residues 19–24 |
| Mature BSA | Residues 25–607 |
| Mature-chain length | 583 amino acids |
| Selected experimental structure | PDB 4F5S |
| Structure method | X-ray diffraction |
| Resolution | 2.47 Å |
| Selected chain | Chain A |
| Working biological form | Monomer |

---

## Structural Model Selection

PDB structure **4F5S** was selected as the initial experimental structure for the BSA molecular dynamics workflow.

The deposited structure contains two BSA chains, A and B. For the current monomeric baseline model, **Chain A** was selected.

The original PDB structure is preserved in:

```text
data/raw/pdb4f5s.ent
```

The initially processed Chain A structure is stored in:

```text
data/processed/4f5s_chainA_BSA.pdb
```

During preprocessing:

- Chain A was retained.
- Chain B was excluded from the monomeric model.
- crystallographic water molecules were excluded.
- the crystallization-associated PGE ligand was excluded.
- the protein residue composition was validated.
- cysteine and disulfide connectivity were inspected.

The original experimental structure is preserved separately so that all subsequent modifications remain traceable.

---

## UniProt Sequence Preparation

The reviewed BSA sequence was obtained from **UniProt P02769 (ALBU_BOVIN)**.

The complete UniProt sequence contains **607 amino acids** and represents the BSA precursor.

The biologically mature albumin chain corresponds to:

```text
UniProt residues 25–607
```

giving:

```text
583 amino acids
```

The full precursor FASTA is stored in:

```text
data/raw/P02769_BSA_full_sequence.fasta
```

The mature sequence was extracted reproducibly using:

```text
scripts/extract_mature_bsa.py
```

The resulting mature-chain FASTA is:

```text
data/processed/P02769_BSA_mature_25-607.fasta
```

The extraction script verifies:

```text
Full precursor length : 607
Mature BSA length     : 583
First 10 residues     : DTHKSEIAHR
Last 10 residues      : LVVSTQTALA
```

---

## PDB Inspection and Validation

The raw 4F5S structure was inspected computationally before MD preparation.

### Initial structural inspection

The inspection showed that:

- Chains A and B each represent the mature BSA chain.
- Each chain contains 583 residues.
- the structure contains crystallographic water molecules.
- a PGE molecule is present in the deposited structure.
- BSA contains 35 cysteine residues per chain.
- 34 cysteines participate in 17 intramolecular disulfide bonds.
- one cysteine remains unpaired.

The scripts used during this stage include:

```text
scripts/01_inspect_pdb.py
scripts/02_extract_bsa_monomer.py
scripts/03_validate_bsa_monomer.py
scripts/04_check_disulfides.py
```

---

## Disulfide-Bond Validation

BSA contains extensive intramolecular disulfide connectivity that contributes strongly to albumin structural stability.

The 4F5S structure contains **17 disulfide bonds per BSA chain**.

The processed Chain A model was checked against the disulfide records of the original PDB structure.

All 17 expected disulfide pairs were found in the processed structure.

The validation also identified:

```text
Total cysteines: 35
Cysteines involved in disulfide bonds: 34
Free cysteine: mature-chain residue 34
```

Because the PDB structure uses mature-chain numbering, mature-chain residue 34 corresponds to **UniProt canonical residue 58**.

Disulfide connectivity will also need to be represented correctly during molecular dynamics topology generation.

---

## Sequence Validation Against UniProt

Before MD topology generation, the amino-acid sequence represented by the processed PDB structure was compared with the mature canonical sequence of UniProt P02769.

The comparison is performed using:

```text
scripts/05_compare_sequence_to_pdb.py
```

Alternate-location atoms in the crystallographic structure are handled during sequence extraction so that each residue is counted only once.

The initial comparison produced:

```text
UniProt mature sequence length : 583
4F5S Chain A sequence length   : 583

Sequence mismatches found: 1

PDB residue 190
UniProt canonical residue 214

UniProt: ALA
4F5S:    THR

Sequence identity: 99.83%
```

Thus, the experimental 4F5S Chain A structure differs from the canonical UniProt P02769 mature sequence at one residue.

---

## Restoration of the Canonical BSA Sequence

For the baseline canonical BSA model, the documented 4F5S sequence difference was restored:

```text
THR 190 → ALA 190
```

in mature-chain/PDB numbering.

This corresponds to:

```text
UniProt residue 214
```

The conversion was performed reproducibly using:

```text
scripts/06_restore_canonical_variant.py
```

For the THR-to-ALA conversion:

- backbone atoms N, CA, C, and O were retained,
- the CB atom was retained,
- THR-specific atoms OG1 and CG2 were removed,
- the residue was renamed from THR to ALA.

The original processed experimental structure was **not overwritten**.

The canonical structure was written to:

```text
data/processed/4f5s_chainA_BSA_canonical.pdb
```

---

## Final Canonical Sequence Validation

The newly generated canonical structure was compared again with the mature UniProt P02769 sequence.

Final validation:

```text
UniProt mature sequence length : 583
4F5S Chain A sequence length   : 583

PASS - UniProt mature BSA and 4F5S Chain A are identical.

Sequence identity: 100.00%
```

Therefore, the current canonical working structure contains the complete **583-residue mature BSA sequence** matching UniProt P02769.

This structure is the planned starting model for subsequent molecular dynamics preparation:

```text
data/processed/4f5s_chainA_BSA_canonical.pdb
```

---

## Structure-Preparation Workflow

The completed workflow is:

```text
UniProt P02769
      │
      ├── Full precursor sequence
      │       607 aa
      │
      └── Mature BSA
              residues 25–607
              583 aa
                    │
                    ▼
              PDB 4F5S
                    │
                    ▼
          Raw structure inspection
                    │
                    ▼
             Select Chain A
                    │
                    ▼
       Remove Chain B / PGE / waters
                    │
                    ▼
        Validate 583-residue structure
                    │
                    ▼
        Validate cysteine residues
          and 17 disulfide bonds
                    │
                    ▼
       Compare sequence with P02769
                    │
                    ▼
       One difference identified
          THR190 vs ALA214
                    │
                    ▼
          Restore canonical ALA
                    │
                    ▼
        Revalidate against UniProt
                    │
                    ▼
        583 / 583 residues matched
          100.00% sequence identity
                    │
                    ▼
       Canonical BSA working model
                    │
                    ▼
          MD system preparation
              [NEXT PHASE]
```

---

## Repository Structure

```text
FTMC-BSA-PEF-MD/
│
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   │   ├── pdb4f5s.ent
│   │   └── P02769_BSA_full_sequence.fasta
│   │
│   └── processed/
│       ├── 4f5s_chainA_BSA.pdb
│       ├── 4f5s_chainA_BSA_canonical.pdb
│       └── P02769_BSA_mature_25-607.fasta
│
├── scripts/
│   ├── 01_inspect_pdb.py
│   ├── 02_extract_bsa_monomer.py
│   ├── 03_validate_bsa_monomer.py
│   ├── 04_check_disulfides.py
│   ├── 05_compare_sequence_to_pdb.py
│   ├── 06_restore_canonical_variant.py
│   └── extract_mature_bsa.py
│
├── simulations/
│   ├── control/
│   └── electric_field/
│
├── analysis/
│
├── figures/
│
└── docs/
    └── internship_notebook.md
```

Additional files and directories will be added as the MD workflow develops.

---

## Current Project Status

### Completed

- Literature collection and initial evidence review
- Selection of BSA as the model protein
- Selection of UniProt P02769
- Selection of PDB 4F5S as the initial experimental structure
- Raw PDB inspection
- Chain A extraction
- Removal of Chain B, PGE, and crystallographic waters from the working monomer
- Residue-count validation
- Cysteine inspection
- Validation of 17 disulfide bonds
- Extraction of the 583-aa mature UniProt BSA sequence
- PDB-to-UniProt sequence comparison
- Identification of the THR190 / canonical ALA214 difference
- Restoration of the canonical alanine residue
- Final sequence validation
- Generation of a canonical 583-residue BSA structure
- 100.00% sequence identity with mature UniProt P02769

### Next Phase

The next phase is **baseline molecular dynamics system preparation**.

Planned steps include:

1. GROMACS environment verification
2. topology generation
3. force-field selection
4. water-model selection
5. protonation-state assessment
6. disulfide-bond representation in the topology
7. simulation-box definition
8. solvation
9. ion addition and system neutralization
10. energy minimization
11. NVT equilibration
12. NPT equilibration
13. baseline/control production MD
14. structural trajectory analysis
15. electric-field simulation design
16. PEF/electric-field simulations
17. comparison of control and field-exposed trajectories

The electric-field simulations will be introduced **only after a stable and validated control simulation has been established**.

---

## Planned MD Analyses

The principal structural and dynamical metrics are expected to include:

### RMSD

Root-mean-square deviation will be used to assess overall structural deviation and conformational stability during simulation.

### RMSF

Root-mean-square fluctuation will be used to identify flexible and field-responsive residues or regions.

### Radius of Gyration

Radius of gyration will be used to assess changes in overall protein compactness.

### SASA

Solvent-accessible surface area will be used to investigate changes in solvent exposure and possible exposure of previously buried regions.

### Hydrogen Bonds

Intramolecular and potentially protein–solvent hydrogen bonding will be examined to investigate changes in structural interactions.

### Secondary Structure

Secondary-structure evolution will be monitored to identify possible changes in α-helical, turn, and coil content.

### Dipole Response

Protein dipole magnitude and/or orientation may be evaluated during electric-field simulations to investigate field-induced molecular response.

---

## Experimental–Computational Interpretation

Experimental PEF studies and atomistic MD simulations operate on substantially different spatial and temporal scales.

Therefore:

> **Experimental electric-field strengths and pulse durations will not be assumed to correspond directly to MD electric-field parameters.**

Simulation conditions will instead be selected based on:

- published protein electric-field MD studies,
- physically meaningful molecular-scale field regimes,
- structural response thresholds,
- computational feasibility,
- and relevance to the experimental observations.

Any mapping between experimental PEF conditions and simulation conditions will be explicitly documented with its assumptions and limitations.

---

## Experimental Context

The computational work is intended to help interpret experimental observations of PEF-induced changes in BSA and related protein systems.

Experimental observables of interest include:

- particle or hydrodynamic size,
- zeta potential,
- fluorescence changes,
- FTIR-derived structural changes,
- secondary-structure alterations,
- aggregation behaviour,
- and changes in intermolecular interactions.

The MD simulations will investigate molecular-scale mechanisms that may help explain these observations rather than attempting to reproduce every experimental measurement directly.

---

## Reproducibility

Reproducibility is a central goal of this repository.

The workflow therefore follows several principles:

- raw structural data are preserved separately from processed structures,
- the original experimental PDB is not overwritten,
- sequence processing is performed using scripts,
- structural modifications are scripted rather than performed only manually,
- validation steps are recorded,
- canonical and experimental structures are stored separately,
- simulation conditions will be documented,
- control simulations will precede electric-field simulations,
- analysis scripts and important derived outputs will be version-controlled where appropriate.

Large MD trajectory files and confidential or unpublished experimental FTMC data should not be committed to the public repository.

---

## Key Literature Context

The project is informed by experimental and computational studies examining protein responses to electric fields and pulsed electric fields.

Particular attention is being given to studies involving:

- BSA under nanosecond pulsed electric fields,
- BSA structural and colloidal changes under electric-field treatment,
- molecular dynamics simulations of proteins exposed to external electric fields,
- field-induced protein unfolding and dipole reorientation,
- and relationships between protein structural changes and experimentally measurable functional properties.

A structured literature database is maintained separately as part of the internship documentation.

---

## Software and Tools

Current or planned computational tools include:

- Python
- pandas
- molecular-structure parsing and validation scripts
- Git
- GitHub
- Visual Studio Code
- WSL Ubuntu
- GROMACS
- molecular trajectory analysis tools

Additional analysis tools may be introduced as required.

---

## Important Numbering Note

Two residue-numbering systems occur in this project.

### UniProt canonical numbering

The complete P02769 precursor contains 607 residues.

```text
Mature BSA = UniProt residues 25–607
```

### Mature-chain / processed PDB numbering

The processed structure begins with the first residue of mature BSA:

```text
PDB mature residue 1 = UniProt residue 25
```

Therefore:

```text
UniProt canonical position = mature-chain position + 24
```

For example:

```text
PDB/mature residue 190
=
UniProt canonical residue 214
```

This distinction should be maintained when reporting residues throughout the project.

---

## Internship Context

This project is being developed as part of a research internship at the:

**Center for Physical Sciences and Technology (FTMC)**  
Vilnius, Lithuania

The internship focuses on combining literature evidence, protein structural analysis, and computational modelling to investigate the effects of pulsed electric fields on protein structure.

---

## Author

**Ahmed Yomi Isiaka**

MSc Systems Biology  
Vilnius University  
Faculty of Medicine

Internship host:  
Center for Physical Sciences and Technology (FTMC), Vilnius

---

## Project Status

**Active research project — structure preparation completed; baseline molecular dynamics preparation is the next stage.**

Results, simulation parameters, analysis workflows, and documentation will be updated as the project progresses.
