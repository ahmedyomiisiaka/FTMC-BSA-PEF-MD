
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Parameters
pulse_us = 50.0
rise_us = 0.3
fall_us = 1.0
field_kv_cm = 5.7

# Assumption: 50 us includes rise, plateau and fall
plateau_us = pulse_us - rise_us - fall_us

assert plateau_us > 0

# Include the exact phase boundaries
t = np.unique(np.concatenate([
    np.linspace(0, rise_us, 301),
    np.linspace(rise_us, rise_us + plateau_us, 1001),
    np.linspace(rise_us + plateau_us, pulse_us, 1001),
]))

# Idealised trapezoidal waveform
E = np.interp(
    t,
    [0, rise_us, rise_us + plateau_us, pulse_us],
    [0, field_kv_cm, field_kv_cm, 0]
)

# Validate the phase boundaries
assert np.isclose(np.interp(rise_us, t, E), field_kv_cm)
assert np.isclose(
    np.interp(rise_us + plateau_us, t, E),
    field_kv_cm
)
assert np.isclose(E[0], 0)
assert np.isclose(E[-1], 0)

# Save results
data_dir = Path("analysis/pef_waveform")
figure_dir = Path("figures/pef_waveform")

data_dir.mkdir(parents=True, exist_ok=True)
figure_dir.mkdir(parents=True, exist_ok=True)

np.savetxt(
    data_dir / "pef_waveform.csv",
    np.column_stack((t, E)),
    delimiter=",",
    header="time_us,electric_field_kV_per_cm",
    comments=""
)

plt.figure(figsize=(10, 5))
plt.plot(t, E, color="navy", linewidth=2)
plt.axvline(rise_us, color="gray", linestyle="--")
plt.axvline(
    rise_us + plateau_us,
    color="gray",
    linestyle="--"
)

plt.xlabel("Time (microseconds)")
plt.ylabel("Electric field (kV/cm)")
plt.title("Proposed 50 us PEF waveform for BSA")
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    figure_dir / "pef_waveform_50us.png",
    dpi=300
)
plt.close()

print("Waveform generated successfully")
print(f"Rising phase: {rise_us} us")
print(f"Plateau phase: {plateau_us} us")
print(f"Falling phase: {fall_us} us")
print(f"Total duration: {pulse_us} us")
print(f"Maximum electric field: {E.max()} kV/cm")
print(f"Number of waveform samples: {len(t)}")


# Detailed visualisation of the three pulse phases
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Full pulse
axes[0].plot(t, E, color="navy", linewidth=2)
axes[0].set_title("Complete PEF pulse (50 us)")
axes[0].set_xlim(0, 50)
axes[0].set_ylim(-0.2, 6.2)

# Rising phase
axes[1].plot(t, E, color="darkgreen", linewidth=2)
axes[1].set_title("Rising phase (300 ns)")
axes[1].set_xlim(0, 0.3)
axes[1].set_ylim(-0.2, 6.2)

# Falling phase
axes[2].plot(t, E, color="darkred", linewidth=2)
axes[2].set_title("Falling phase (1000 ns)")
axes[2].set_xlim(49, 50)
axes[2].set_ylim(-0.2, 6.2)

for ax in axes:
    ax.set_xlabel("Time (microseconds)")
    ax.set_ylabel("Electric field (kV/cm)")
    ax.grid(alpha=0.3)

fig.suptitle(
    "Proposed BSA-PEF waveform: 5.7 kV/cm",
    fontsize=14
)
fig.tight_layout()

fig.savefig(
    figure_dir / "pef_waveform_three_phases.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close(fig)

print("Three-phase waveform figure saved successfully")
