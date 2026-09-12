from pathlib import Path

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------

fasta_file = Path("data/processed/P02769_BSA_mature_25-607.fasta")
pdb_file = Path("data/processed/4f5s_chainA_BSA_canonical.pdb")

# ------------------------------------------------------------
# Standard amino-acid conversion
# ------------------------------------------------------------

three_to_one = {
    "ALA": "A",
    "ARG": "R",
    "ASN": "N",
    "ASP": "D",
    "CYS": "C",
    "GLN": "Q",
    "GLU": "E",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LEU": "L",
    "LYS": "K",
    "MET": "M",
    "PHE": "F",
    "PRO": "P",
    "SER": "S",
    "THR": "T",
    "TRP": "W",
    "TYR": "Y",
    "VAL": "V",
}

# ------------------------------------------------------------
# Read mature UniProt FASTA sequence
# ------------------------------------------------------------

with fasta_file.open() as f:
    fasta_lines = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith(">")
    ]

uniprot_sequence = "".join(fasta_lines)

# ------------------------------------------------------------
# Extract Chain A sequence from processed PDB
#
# We use one CA atom per residue.
# For alternate locations, keep:
#   blank altLoc
#   altLoc A
# and ignore altLoc B or others.
# ------------------------------------------------------------

pdb_residues = []

with pdb_file.open() as f:
    for line in f:
        if not line.startswith("ATOM"):
            continue

        atom_name = line[12:16].strip()
        altloc = line[16].strip()
        residue_name = line[17:20].strip()
        chain = line[21].strip()
        residue_number = int(line[22:26].strip())

        if chain == "A" and atom_name == "CA" and altloc in ("", "A"):

            if residue_name not in three_to_one:
                raise ValueError(
                    f"Unknown residue {residue_name} "
                    f"at PDB position {residue_number}"
                )

            pdb_residues.append(
                (
                    residue_number,
                    three_to_one[residue_name],
                    residue_name,
                )
            )

pdb_sequence = "".join(
    residue[1] for residue in pdb_residues
)

# ------------------------------------------------------------
# Basic checks
# ------------------------------------------------------------

print("=" * 70)
print("BSA SEQUENCE COMPARISON")
print("=" * 70)

print(f"UniProt mature sequence length : {len(uniprot_sequence)}")
print(f"4F5S Chain A sequence length   : {len(pdb_sequence)}")

print()
print(f"UniProt first 10 residues      : {uniprot_sequence[:10]}")
print(f"PDB first 10 residues          : {pdb_sequence[:10]}")

print()
print(f"UniProt last 10 residues       : {uniprot_sequence[-10:]}")
print(f"PDB last 10 residues           : {pdb_sequence[-10:]}")

# ------------------------------------------------------------
# Compare sequences residue by residue
#
# PDB mature residue 1 corresponds to UniProt residue 25.
# Therefore:
# UniProt canonical position = mature position + 24
# ------------------------------------------------------------

mismatches = []

comparison_length = min(
    len(uniprot_sequence),
    len(pdb_sequence)
)

for i in range(comparison_length):

    uni_aa = uniprot_sequence[i]
    pdb_aa = pdb_sequence[i]

    if uni_aa != pdb_aa:

        pdb_position = pdb_residues[i][0]
        uniprot_position = i + 25

        mismatches.append(
            (
                pdb_position,
                uniprot_position,
                uni_aa,
                pdb_aa,
            )
        )

# ------------------------------------------------------------
# Report result
# ------------------------------------------------------------

print()
print("-" * 70)

if len(uniprot_sequence) != len(pdb_sequence):
    print("WARNING: Sequence lengths are different.")

if (
    len(uniprot_sequence) == len(pdb_sequence)
    and len(mismatches) == 0
):
    print(
        "PASS - UniProt mature BSA and "
        "4F5S Chain A are identical."
    )

else:
    print(f"Sequence mismatches found: {len(mismatches)}")

    for pdb_pos, uni_pos, uni_aa, pdb_aa in mismatches:
        print(
            f"PDB residue {pdb_pos} "
            f"(UniProt residue {uni_pos}): "
            f"UniProt={uni_aa}, PDB={pdb_aa}"
        )

print("-" * 70)

if max(len(uniprot_sequence), len(pdb_sequence)) > 0:

    matches = sum(
        1
        for i in range(comparison_length)
        if uniprot_sequence[i] == pdb_sequence[i]
    )

    identity = (
        matches
        / max(
            len(uniprot_sequence),
            len(pdb_sequence)
        )
        * 100
    )

else:
    identity = 0.0

print(f"Sequence identity: {identity:.2f}%")
print("=" * 70)