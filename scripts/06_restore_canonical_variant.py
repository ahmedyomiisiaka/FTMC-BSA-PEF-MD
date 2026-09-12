from pathlib import Path

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------

input_pdb = Path("data/processed/4f5s_chainA_BSA.pdb")
output_pdb = Path("data/processed/4f5s_chainA_BSA_canonical.pdb")

# ------------------------------------------------------------
# Variant to restore
#
# 4F5S:
#   mature-chain residue 190 = THR
#
# UniProt P02769 canonical sequence:
#   mature-chain residue 190 = ALA
#   canonical UniProt residue 214 = ALA
#
# THR -> ALA requires:
#   keep backbone atoms N, CA, C, O
#   keep CB
#   remove THR-specific OG1 and CG2 atoms
#   rename residue THR -> ALA
# ------------------------------------------------------------

target_chain = "A"
target_residue_number = 190
old_residue = "THR"
new_residue = "ALA"

# Atoms that belong to alanine
allowed_atoms = {
    "N",
    "CA",
    "C",
    "O",
    "CB",
}

changed_atoms = 0
removed_atoms = 0
found_target = False

output_lines = []

with input_pdb.open() as f:
    for line in f:

        # Keep all non-ATOM records unchanged
        if not line.startswith("ATOM"):
            output_lines.append(line)
            continue

        atom_name = line[12:16].strip()
        residue_name = line[17:20].strip()
        chain = line[21].strip()
        residue_number = int(line[22:26].strip())

        is_target = (
            chain == target_chain
            and residue_number == target_residue_number
            and residue_name == old_residue
        )

        if not is_target:
            output_lines.append(line)
            continue

        found_target = True

        # Remove THR-specific side-chain atoms
        if atom_name not in allowed_atoms:
            removed_atoms += 1
            continue

        # Rename THR to ALA while preserving PDB formatting
        new_line = (
            line[:17]
            + f"{new_residue:>3}"
            + line[20:]
        )

        output_lines.append(new_line)
        changed_atoms += 1

# ------------------------------------------------------------
# Safety checks
# ------------------------------------------------------------

if not found_target:
    raise RuntimeError(
        "Target residue THR A 190 was not found."
    )

if changed_atoms != 5:
    raise RuntimeError(
        f"Expected 5 retained ALA atoms, found {changed_atoms}."
    )

if removed_atoms != 2:
    raise RuntimeError(
        f"Expected to remove 2 THR-specific atoms, "
        f"removed {removed_atoms}."
    )

# ------------------------------------------------------------
# Write canonical structure
# ------------------------------------------------------------

with output_pdb.open("w") as f:
    f.writelines(output_lines)

print("=" * 70)
print("CANONICAL BSA VARIANT RESTORATION")
print("=" * 70)

print(f"Input structure : {input_pdb}")
print(f"Output structure: {output_pdb}")

print()
print(
    "Restored variant: "
    "THR 190 -> ALA 190 "
    "(UniProt canonical residue 214)"
)

print(f"Atoms retained and renamed : {changed_atoms}")
print(f"THR-specific atoms removed : {removed_atoms}")

print()
print("Removed atoms: OG1 and CG2")
print("Retained atoms: N, CA, C, O, CB")

print()
print(
    "PASS - canonical Ala190 structure created "
    "without overwriting the original PDB."
)

print("=" * 70)