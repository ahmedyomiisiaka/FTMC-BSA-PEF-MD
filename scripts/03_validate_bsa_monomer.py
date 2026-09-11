from pathlib import Path
from collections import Counter

pdb_file = Path("data/processed/4f5s_chainA_BSA.pdb")

atoms = 0
residues = set()
chains = set()
residue_names = Counter()
hetatm = []
cysteines = set()

with pdb_file.open() as f:
    for line in f:

        record = line[0:6].strip()

        if record == "ATOM":

            atoms += 1

            residue_name = line[17:20].strip()
            chain = line[21].strip()
            residue_number = line[22:26].strip()

            chains.add(chain)

            residues.add(
                (chain, residue_number, residue_name)
            )

            residue_names[residue_name] += 1

            if residue_name == "CYS":
                cysteines.add(
                    (chain, residue_number)
                )

        elif record == "HETATM":
            hetatm.append(line.strip())


print("=== BSA MONOMER VALIDATION ===")

print(f"\nFile: {pdb_file}")

print(f"\nProtein atoms: {atoms}")

print(f"Protein residues: {len(residues)}")

print(f"Chains present: {sorted(chains)}")

print(f"HETATM records: {len(hetatm)}")

print(f"Cysteine residues: {len(cysteines)}")


numbers = sorted(
    int(residue_number)
    for chain, residue_number, residue_name in residues
)

print(
    f"Residue-number range: "
    f"{min(numbers)}-{max(numbers)}"
)


print("\nCysteine positions:")

print(
    ", ".join(
        residue_number
        for chain, residue_number
        in sorted(
            cysteines,
            key=lambda x: int(x[1])
        )
    )
)


print("\nValidation checks:")

if chains == {"A"}:
    print("PASS - only Chain A is present")
else:
    print("CHECK - unexpected chains detected")


if len(residues) == 583:
    print("PASS - expected 583 BSA residues present")
else:
    print(
        f"CHECK - expected 583 residues, "
        f"found {len(residues)}"
    )


if len(hetatm) == 0:
    print("PASS - no HETATM records present")
else:
    print(
        f"CHECK - {len(hetatm)} HETATM records remain"
    )


if len(cysteines) == 35:
    print("PASS - expected 35 cysteine residues present")
else:
    print(
        f"CHECK - found {len(cysteines)} cysteine residues"
    )