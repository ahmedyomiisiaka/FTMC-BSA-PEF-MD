import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Read GROMACS RMSF data and remove metadata.
with open("rmsf_recovery.xvg") as file:
    lines = [
        line for line in file
        if line.strip() and not line.lstrip().startswith(("#", "@"))
    ]

data = pd.read_csv(
    StringIO("".join(lines)),
    sep=r"\s+",
    header=None,
    names=["Residue", "RMSF_nm"]
)

# Calculate statistics.
mean_rmsf = data["RMSF_nm"].mean()
max_row = data.loc[data["RMSF_nm"].idxmax()]

# Create graph.
fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    data["Residue"],
    data["RMSF_nm"],
    color="purple",
    linewidth=1.3,
    label="BSA residue RMSF"
)

ax.axhline(
    mean_rmsf,
    color="red",
    linestyle="--",
    label=f"Mean RMSF = {mean_rmsf:.4f} nm"
)

ax.scatter(
    max_row["Residue"],
    max_row["RMSF_nm"],
    color="darkorange",
    s=45,
    zorder=3,
    label=f"Highest RMSF: residue {int(max_row['Residue'])}"
)

ax.set_xlabel("BSA residue number")
ax.set_ylabel("RMSF (nm)")
ax.set_title("BSA Residue Flexibility — Electric-Field Recovery Segment")
ax.legend()
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("rmsf_recovery.png", dpi=300)
plt.close(fig)

print(f"Residues analyzed: {len(data)}")
print(f"Mean RMSF: {mean_rmsf:.4f} nm")
print(f"Maximum RMSF: {max_row['RMSF_nm']:.4f} nm")
print(f"Most flexible residue: {int(max_row['Residue'])}")
print("Graph saved: rmsf_recovery.png")
