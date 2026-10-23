import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Read the GROMACS SASA file, excluding metadata.
with open("sasa_recovery.xvg") as file:
    lines = [
        line for line in file
        if line.strip() and not line.lstrip().startswith(("#", "@"))
    ]

data = pd.read_csv(
    StringIO("".join(lines)),
    sep=r"\s+",
    header=None,
    names=["Time_ps", "SASA_nm2"]
)

# Convert picoseconds to nanoseconds.
data["Time_ns"] = data["Time_ps"] / 1000

# Calculate descriptive statistics.
mean_sasa = data["SASA_nm2"].mean()
min_sasa = data["SASA_nm2"].min()
max_sasa = data["SASA_nm2"].max()
final_sasa = data["SASA_nm2"].iloc[-1]

# Create the graph.
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(
    data["Time_ns"],
    data["SASA_nm2"],
    color="darkorange",
    linewidth=1.8,
    label="BSA total SASA"
)

ax.axhline(
    mean_sasa,
    color="red",
    linestyle="--",
    label=f"Mean SASA = {mean_sasa:.2f} nm²"
)

ax.set_xlabel("Simulation time (ns)")
ax.set_ylabel("Solvent-accessible surface area (nm²)")
ax.set_title("BSA Solvent-Accessible Surface Area — Electric-Field Recovery Segment")
ax.legend()
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("sasa_recovery.png", dpi=300)
plt.close(fig)

print(f"Frames analyzed: {len(data)}")
print(f"Mean SASA: {mean_sasa:.3f} nm²")
print(f"Minimum SASA: {min_sasa:.3f} nm²")
print(f"Maximum SASA: {max_sasa:.3f} nm²")
print(f"Final SASA: {final_sasa:.3f} nm²")
print("Graph saved: sasa_recovery.png")
