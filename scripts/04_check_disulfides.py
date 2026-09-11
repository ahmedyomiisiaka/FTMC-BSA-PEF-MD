from pathlib import Path

raw_pdb = Path("data/raw/pdb4f5s.ent")
processed_pdb = Path("data/processed/4f5s_chainA_BSA.pdb")

expected_pairs = []

# Read Chain A disulfide bonds from original PDB
with raw_pdb.open() as f:
    for line in f:

        if line.startswith("SSBOND"):

            chain1 = line[15].strip()
            res1 = line[17:21].strip()

            chain2 = line[29].strip()
            res2 = line[31:35].strip()

            if chain1 == "A" and chain2 == "A":
                expected_pairs.append(
                    (int(res1), int(res2))
                )


# Identify cysteine residues in processed structure
cysteines = set()

with processed_pdb.open() as f:
    for line in f:

        if line.startswith("ATOM"):

            residue_name = line[17:20].strip()
            chain = line[21].strip()
            residue_number = line[22:26].strip()

            if residue_name == "CYS" and chain == "A":
                cysteines.add(int(residue_number))


print("=== BSA DISULFIDE CHECK ===")

print(f"\nDisulfide bonds from original 4F5S: {len(expected_pairs)}")

for res1, res2 in expected_pairs:
    print(f"CYS {res1} -- CYS {res2}")


print("\nChecking that both cysteines are present:")

all_present = True

for res1, res2 in expected_pairs:

    if res1 in cysteines and res2 in cysteines:
        print(f"PASS - {res1}-{res2}")
    else:
        print(f"CHECK - missing cysteine in pair {res1}-{res2}")
        all_present = False


paired_cysteines = {
    residue
    for pair in expected_pairs
    for residue in pair
}

free_cysteines = cysteines - paired_cysteines


print("\nSummary")

print(f"Total cysteine residues: {len(cysteines)}")
print(f"Cysteines involved in disulfides: {len(paired_cysteines)}")
print(f"Free cysteines: {sorted(free_cysteines)}")


if len(expected_pairs) == 17 and all_present:
    print("\nPASS - all 17 Chain A disulfide bonds can be reconstructed.")
else:
    print("\nCHECK - disulfide information requires further inspection.")