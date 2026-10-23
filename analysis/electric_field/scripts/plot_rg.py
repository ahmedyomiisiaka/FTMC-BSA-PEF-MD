import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Read the GROMACS file, ignoring metadata.
with open("rg_recovery.xvg") as file:
    lines = [
        line for line in file
        if line.strip() and not line.lstrip().startswith(("#", "@"))
    ]

data = pd.read_csv(
    StringIO("".join(lines)),
    sep=r"\s+",
    header=None,
    names=["Time_ps", "Rg_nm", "Rg_X", "Rg_Y", "Rg_Z"]
)

# Convert picoseconds to nanoseconds.
data["Time_ns"] = data["Time_ps"] / 1000

# Calculate statistics.
mean_rg = data["Rg_nm"].mean()
min_rg = data["Rg_nm"].min()
max_rg = data["Rg_nm"].max()
final_rg = data["Rg_nm"].iloc[-1]

# Create the graph.
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    data["Time_ns"],
    data["Rg_nm"],
    color="darkgreen",
    linewidth=1.8,
    label="BSA total Rg"
)

ax.axhline(
    mean_rg,
    color="red",
    linestyle="--",
    label=f"Mean Rg = {mean_rg:.4f} nm"
)

ax.set_xlabel("Simulation time (ns)")
ax.set_ylabel("Radius of gyration (nm)")
ax.set_title("BSA Radius of Gyration — Electric-Field Recovery Segment")
ax.legend()
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("rg_recovery.png", dpi=300)
plt.close(fig)

print(f"Frames analyzed: {len(data)}")
print(f"Mean Rg: {mean_rg:.4f} nm")
print(f"Minimum Rg: {min_rg:.4f} nm")
print(f"Maximum Rg: {max_rg:.4f} nm")
print(f"Final Rg: {final_rg:.4f} nm")
print("Graph saved: rg_recovery.png")
