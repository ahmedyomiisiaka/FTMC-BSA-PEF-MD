from pathlib import Path

input_file = Path("data/raw/P02769_BSA_full_sequence.fasta")
output_file = Path("data/processed/P02769_BSA_mature_25-607.fasta")

# Read FASTA
with open(input_file, "r") as f:
    lines = f.readlines()

header = lines[0].strip()

# Join sequence lines and remove whitespace
full_sequence = "".join(line.strip() for line in lines[1:])

print("UniProt accession: P02769")
print("Full precursor length:", len(full_sequence))

# UniProt mature chain = residues 25-607.
# Python indexing begins at 0, so residue 25 is index 24.
mature_sequence = full_sequence[24:607]

print("Mature BSA length:", len(mature_sequence))
print("First 10 mature residues:", mature_sequence[:10])
print("Last 10 mature residues:", mature_sequence[-10:])

assert len(full_sequence) == 607, "ERROR: precursor should contain 607 residues"
assert len(mature_sequence) == 583, "ERROR: mature BSA should contain 583 residues"

mature_header = (
    ">sp|P02769|ALBU_BOVIN_mature "
    "Albumin mature chain OS=Bos taurus "
    "UniProt_residues=25-607 Length=583"
)

with open(output_file, "w") as f:
    f.write(mature_header + "\n")
    for i in range(0, len(mature_sequence), 60):
        f.write(mature_sequence[i:i+60] + "\n")

print("\nPASS - mature BSA sequence extracted successfully.")
print("Saved:", output_file)