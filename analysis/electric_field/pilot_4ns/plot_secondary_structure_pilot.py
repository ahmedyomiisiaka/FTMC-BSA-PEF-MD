from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

# Project paths
data_file = Path(
    "analysis/electric_field/pilot_4ns/"
    "secondary_structure_pilot_4ns.dat"
)

output_dir = Path("figures/electric_field")
output_dir.mkdir(parents=True, exist_ok=True)

# Read DSSP secondary-structure assignments
lines = [
    line.strip()
    for line in data_file.read_text().splitlines()
    if line.strip()
]

assert len(lines) == 403, "Unexpected number of frames"
assert all(len(line) == 583 for line in lines), \
    "Unexpected residue count"

structure = np.array([list(line) for line in lines])

symbols = ["H", "G", "I", "E", "B", "T", "S", "P", "~"]

names = [
    "Alpha-helix", "3-10 helix", "Pi-helix",
    "Beta-strand", "Beta-bridge", "Turn",
    "Bend", "Polyproline-II", "Coil"
]

colors = [
    "#2878B5", "#5BA4CF", "#A7D4ED",
    "#D54E4E", "#E99A9A", "#E9A23B",
    "#F1D36C", "#8A65BA", "#D0D0D0"
]

counts = Counter(structure.flatten())
total = structure.size

percentages = [
    100 * counts[s] / total
    for s in symbols
]

# ---------------------------------------
# Figure 1: Secondary-structure composition
# ---------------------------------------

fig, ax = plt.subplots(figsize=(10, 5.5))

bars = ax.barh(names, percentages, color=colors)
ax.invert_yaxis()

ax.set_xlabel("Average residue assignments (%)")
ax.set_title(
    "BSA Secondary-Structure Composition — "
    "Original Electric-Field Pilot (4.02 ns)"
)

for bar, value in zip(bars, percentages):
    ax.text(
        bar.get_width() + 0.4,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.2f}%",
        va="center",
        fontsize=9
    )

ax.set_xlim(0, max(percentages) + 10)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

fig.tight_layout()

composition_file = (
    output_dir /
    "secondary_structure_composition_pilot_4ns.png"
)

fig.savefig(composition_file, dpi=300)
plt.close(fig)

# ---------------------------------------
# Figure 2: Secondary-structure heatmap
# ---------------------------------------

symbol_to_number = {
    symbol: i
    for i, symbol in enumerate(symbols)
}

numeric = np.array([
    [symbol_to_number[s] for s in row]
    for row in structure
])

cmap = ListedColormap(colors)

norm = BoundaryNorm(
    np.arange(-0.5, len(symbols) + 0.5),
    cmap.N
)

fig, ax = plt.subplots(figsize=(13, 6))

ax.imshow(
    numeric,
    aspect="auto",
    interpolation="nearest",
    cmap=cmap,
    norm=norm,
    origin="lower",
    extent=[0.5, 583.5, -0.005, 4.025]
)

ax.set_xlabel("BSA residue number")
ax.set_ylabel("Simulation time (ns)")
ax.set_title(
    "BSA Secondary-Structure Evolution — "
    "Original Electric-Field Pilot (4.02 ns)"
)

legend = [
    Patch(facecolor=color, label=name)
    for color, name in zip(colors, names)
]

ax.legend(
    handles=legend,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.13),
    ncol=5,
    fontsize=8
)

fig.tight_layout()

heatmap_file = (
    output_dir /
    "secondary_structure_heatmap_pilot_4ns.png"
)

fig.savefig(
    heatmap_file,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

# Print summary
print(f"Frames analyzed: {len(lines)}")
print(f"Residues per frame: {structure.shape[1]}")
print(f"Total assignments: {total}")

for name, value in zip(names, percentages):
    print(f"{name}: {value:.2f}%")

print(f"Saved: {composition_file}")
print(f"Saved: {heatmap_file}")
