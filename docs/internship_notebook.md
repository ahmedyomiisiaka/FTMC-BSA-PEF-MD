# FTMC BSA–PEF Internship Notebook

## 11 September 2026

### Objective
Begin preparation for computational analysis of bovine serum
albumin (BSA) and its possible response to electric-field/PEF
conditions.

### Literature review
Reviewed literature concerning electric-field effects on proteins,
with particular attention to BSA. Experimental evidence suggests
that moderate electric-field exposure can produce partial structural
changes, while stronger exposure can cause more extensive
denaturation or aggregation.

### Protein identification
Bovine serum albumin was identified using UniProt.

UniProt accession: P02769
Protein: Albumin
Organism: Bos taurus
Canonical precursor length: 607 amino acids
Mature chain: UniProt residues 25–607

### Structural organisation
UniProt divides BSA into three albumin domains:
- Albumin 1: residues 19–209
- Albumin 2: residues 210–402
- Albumin 3: residues 403–600

### Candidate structure
PDB ID: 4F5S
Method: X-ray diffraction
Resolution: 2.47 Å
Rwork: 0.20
Rfree: 0.26

The structure represents mature BSA and contains two protein
chains (A and B). PDBe identifies the preferred biological assembly
as a monomer.

### Coordinate-file inspection
The downloaded 4F5S PDB file was inspected.

Both chain A and chain B contain 583 protein residues,
numbered 1–583, without internal residue-number gaps in the
ATOM records.

The PDB file contains 34 SSBOND records, corresponding to
17 disulfide bonds per BSA chain.

A PGE (triethylene glycol) molecule is associated with chain A,
and crystallographic water molecules are also present.

### Current decision
4F5S will be retained as a candidate starting structure for
baseline BSA molecular-dynamics preparation.

The next step is to prepare a single BSA monomer for an initial
control simulation. Decisions about removal of crystallographic
waters, PGE and other non-protein components will be documented
rather than performed automatically.
