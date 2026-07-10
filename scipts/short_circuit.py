"""
example_short_circuit.py
Worked example of the pattern: theme + physics -> a two-panel static
figure in the same visual language as the out-of-step GIF, but for a
simpler concept (fault current falling off with distance from source).

This is the "level 1" starting point before you attempt animation.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from physics import short_circuit

theme.apply()

# --- inputs ---------------------------------------------------------
V_SOURCE_KV = 13.8
Z_SOURCE = 0.8            # ohms, source impedance
Z_LINE_PER_KM = 0.35       # ohms/km, feeder impedance
distances = np.linspace(0, 10, 200)

i_fault = short_circuit.fault_current_profile(V_SOURCE_KV, Z_SOURCE,
                                               Z_LINE_PER_KM, distances)

# --- layout: hero panel + supporting panel, same bones as the GIF ---
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.25)

ax_main = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# hero panel: fault current vs distance
ax_main.plot(distances, i_fault, color=theme.ACCENT, linewidth=2.5)
ax_main.fill_between(distances, i_fault, color=theme.ACCENT, alpha=0.08)
ax_main.set_xlabel("Fault distance from source (km)")
ax_main.set_ylabel("I_k'' (A)")
ax_main.set_title("Fault current drops fast as you move down the feeder")
ax_main.grid(True, alpha=0.4)

# annotate the "answer" the way the GIF marks the electrical center
i_at_5km = short_circuit.three_phase_fault_current(V_SOURCE_KV, Z_SOURCE,
                                                    Z_LINE_PER_KM, 5.0)
ax_main.scatter([5], [i_at_5km], color=theme.ACCENT, zorder=5, s=60)
ax_main.annotate(f"{i_at_5km:,.0f} A @ 5 km", (5, i_at_5km),
                  xytext=(15, 20), textcoords="offset points",
                  color=theme.FG, fontsize=10, fontfamily=theme.FONT_MONO,
                  arrowprops=dict(arrowstyle="->", color=theme.MUTED))

# side panel: relay-relevant zoom (0-2km, where protection settings matter)
mask = distances <= 2
ax_side.plot(distances[mask], i_fault[mask], color=theme.SERIES[1], linewidth=2)
ax_side.set_title("Zoom: protection zone (0-2 km)", fontsize=11)
ax_side.set_xlabel("km")
ax_side.grid(True, alpha=0.4)

theme.header(fig,
    "Why fault current falls off with distance",
    "Source impedance dominates near the bus; line impedance takes over further out")
theme.footer(fig,
    f"V={V_SOURCE_KV}kV  Zs={Z_SOURCE}Ω  Zline={Z_LINE_PER_KM}Ω/km  "
    "simplified single-source radial model, no c-factor",
    handle="code.arts")

fig.savefig("outputs/short_circuit_example.png", dpi=150)
print("saved short_circuit_example.png")