"""
ohms_law.py
Two-panel Ohm's Law visualization in the same visual language as the
short-circuit example: I = V / R as both a non-linear (I vs R) and
a linear (I vs V) relationship.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from physics import ohms_law

theme.apply()

# --- inputs ---------------------------------------------------------
V_FIXED = 120.0          # volts, typical US residential circuit
R_FIXED = 60.0            # ohms, the "answer" resistance
resistances = np.linspace(5, 200, 300)
voltages    = np.linspace(0, 240, 300)

i_curve = ohms_law.current_profile(V_FIXED, resistances)
i_at_r  = ohms_law.current(V_FIXED, R_FIXED)
p_at_r  = ohms_law.power(V_FIXED, R_FIXED)

# --- layout: hero panel + supporting panel, same bones as the GIF ---
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.25)

ax_main = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# hero panel: current vs resistance at fixed voltage
ax_main.plot(resistances, i_curve, color=theme.ACCENT, linewidth=2.5)
ax_main.fill_between(resistances, i_curve, color=theme.ACCENT, alpha=0.08)
ax_main.set_xlabel("Resistance (Ω)")
ax_main.set_ylabel("Current (A)")
ax_main.set_title("I = V / R — current drops as resistance increases")
ax_main.grid(True, alpha=0.4)

# annotate the "answer"
ax_main.scatter([R_FIXED], [i_at_r], color=theme.ACCENT, zorder=5, s=60)
ax_main.annotate(f"{i_at_r:.2f} A @ {R_FIXED} Ω  ({p_at_r:.0f} W)",
                  (R_FIXED, i_at_r), xytext=(20, 30),
                  textcoords="offset points", color=theme.FG, fontsize=10,
                  fontfamily=theme.FONT_MONO,
                  arrowprops=dict(arrowstyle="->", color=theme.MUTED))

# side panel: current vs voltage at fixed resistance (linear Ohm's Law)
i_linear = voltages / R_FIXED
ax_side.plot(voltages, i_linear, color=theme.SERIES[1], linewidth=2)
ax_side.fill_between(voltages, i_linear, color=theme.SERIES[1], alpha=0.08)
ax_side.scatter([V_FIXED], [i_at_r], color=theme.SERIES[1], zorder=5, s=60)
ax_side.set_title("I = V / R — linear at fixed R", fontsize=11)
ax_side.set_xlabel("Voltage (V)")
ax_side.set_ylabel("Current (A)")
ax_side.grid(True, alpha=0.4)

theme.header(fig,
    "Ohm's Law: two ways to see I = V / R",
    "Left: hyperbola at fixed voltage — Right: straight line at fixed resistance")
theme.footer(fig,
    f"V={V_FIXED}V  R={R_FIXED}Ω  I={i_at_r:.2f}A  P={p_at_r:.0f}W  "
    "DC resistive circuit, no temperature effects",
    handle="code.arts")

fig.savefig("outputs/ohms_law.png", dpi=150)
print("saved ohms_law.png")
