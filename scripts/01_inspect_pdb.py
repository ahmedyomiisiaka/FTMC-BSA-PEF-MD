from collections import Counter, defaultdict

pdb_file = "data/raw/pdb4f5s.ent"

protein_residues = defaultdict(set)
hetero_residues = Counter()
water_residues = set()
disulfide_bonds = []

with open(pdb_file, "r") as f:
    for line in f:

        record = line[0:6].strip()

        if record == "ATOM":
            residue_name = line[17:20].strip()
            chain = line[21].strip()
            residue_number = line[22:26].strip()

            protein_residues[chain].add(
                (residue_number, residue_name)
            )

        elif record == "HETATM":
            residue_name = line[17:20].strip()
            chain = line[21].strip()
            residue_number = line[22:26].strip()

            if residue_name == "HOH":
                water_residues.add(
                    (chain, residue_number)
                )
            else:
                hetero_residues[
                    (chain, residue_name, residue_number)
                ] += 1

        elif record == "SSBOND":
            disulfide_bonds.append(line.strip())


print("=== Protein chains ===")

for chain, residues in protein_residues.items():

    numbers = sorted(
        int(residue_number)
        for residue_number, residue_name in residues
    )

    print(
        f"Chain {chain}: "
        f"{len(residues)} residues "
        f"({min(numbers)}-{max(numbers)})"
    )


print("\n=== Non-protein molecules ===")

for item in hetero_residues:
    chain, residue_name, residue_number = item

    print(
        f"{residue_name} "
        f"chain {chain} "
        f"residue {residue_number}"
    )


print("\n=== Crystallographic waters ===")

water_counts = Counter(
    chain for chain, residue_number in water_residues
)

for chain, count in water_counts.items():
    print(f"Chain {chain}: {count} waters")


print("\n=== Disulfide bonds ===")

print(f"Total SSBOND records: {len(disulfide_bonds)}")

for bond in disulfide_bonds:
    print(bond)