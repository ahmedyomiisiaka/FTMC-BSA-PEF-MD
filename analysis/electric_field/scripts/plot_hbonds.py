import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Read the GROMACS hydrogen-bond data.
with open("hbonds_recovery.xvg") as file:
    lines = [
        line for line in file
        if line.strip() and not line.lstrip().startswith(("#", "@"))
    ]

data = pd.read_csv(
    StringIO("".join(lines)),
    sep=r"\s+",
    header=None,
    names=["Time_ps", "Hydrogen_bonds", "Pairs_035nm"]
)

# Convert time from picoseconds to nanoseconds.
data["Time_ns"] = data["Time_ps"] / 1000

# Calculate statistics.
mean_hb = data["Hydrogen_bonds"].mean()
min_hb = data["Hydrogen_bonds"].min()
max_hb = data["Hydrogen_bonds"].max()
final_hb = data["Hydrogen_bonds"].iloc[-1]

# Create the graph.
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    data["Time_ns"],
    data["Hydrogen_bonds"],
    color="teal",
    linewidth=1.8,
    label="Protein–protein hydrogen bonds"
)

ax.axhline(
    mean_hb,
    color="red",
    linestyle="--",
    label=f"Mean = {mean_hb:.2f}"
)

ax.set_xlabel("Simulation time (ns)")
ax.set_ylabel("Number of hydrogen bonds")
ax.set_title("BSA Internal Hydrogen Bonds — Electric-Field Recovery Segment")

ax.legend()
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("hbonds_recovery.png", dpi=300)
plt.close(fig)

print(f"Frames analyzed: {len(data)}")
print(f"Mean hydrogen bonds: {mean_hb:.2f}")
print(f"Minimum hydrogen bonds: {min_hb}")
print(f"Maximum hydrogen bonds: {max_hb}")
print(f"Final hydrogen bonds: {final_hb}")
print("Graph saved: hbonds_recovery.png")
