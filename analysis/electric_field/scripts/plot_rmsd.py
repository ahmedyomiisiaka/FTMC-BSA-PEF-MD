import pandas as pd
import matplotlib.pyplot as plt

# Read the GROMACS RMSD file.
# Skip metadata lines beginning with # or @.
# Read only numerical data, ignoring GROMACS metadata.
with open("rmsd_recovery.xvg") as file:
    lines = [
        line for line in file
        if line.strip() and not line.lstrip().startswith(("#", "@"))
    ]

from io import StringIO

data = pd.read_csv(
    StringIO("".join(lines)),
    sep=r"\s+",
    header=None,
    names=["Time_ns", "RMSD_nm"]
)

# Calculate statistics.
mean_rmsd = data["RMSD_nm"].mean()

# Create the figure.
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    data["Time_ns"],
    data["RMSD_nm"],
    linewidth=1.8,
    color="navy",
    label="BSA backbone RMSD"
)

ax.axhline(
    mean_rmsd,
    linestyle="--",
    color="red",
    label=f"Mean RMSD = {mean_rmsd:.4f} nm"
)

ax.set_xlabel("Simulation time (ns)")
ax.set_ylabel("Backbone RMSD (nm)")
ax.set_title("BSA Backbone RMSD — Electric-Field Recovery Segment")
ax.legend()
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("rmsd_recovery.png", dpi=300)
plt.close(fig)

print(f"Frames analyzed: {len(data)}")
print(f"Mean RMSD: {mean_rmsd:.4f} nm")
print("Graph saved: rmsd_recovery.png")
