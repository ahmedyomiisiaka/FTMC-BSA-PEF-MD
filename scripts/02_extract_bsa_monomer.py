from pathlib import Path

input_file = Path("data/raw/pdb4f5s.ent")
output_file = Path("data/processed/4f5s_chainA_BSA.pdb")

output_file.parent.mkdir(parents=True, exist_ok=True)

kept_atoms = 0
removed_heteroatoms = 0

with input_file.open() as infile, output_file.open("w") as outfile:

    outfile.write("REMARK   Clean BSA monomer extracted from PDB 4F5S\n")
    outfile.write("REMARK   Chain A protein atoms retained\n")
    outfile.write("REMARK   Chain B, PGE and crystallographic waters excluded\n")

    for line in infile:

        record = line[0:6].strip()

        # Keep only protein ATOM records belonging to chain A
        if record == "ATOM" and line[21] == "A":
            outfile.write(line)
            kept_atoms += 1

        elif record == "HETATM":
            removed_heteroatoms += 1

    outfile.write("TER\n")
    outfile.write("END\n")


print("BSA monomer extraction complete.")
print(f"Input:  {input_file}")
print(f"Output: {output_file}")
print(f"Protein atoms retained: {kept_atoms}")
print(f"HETATM records excluded from working structure: {removed_heteroatoms}")