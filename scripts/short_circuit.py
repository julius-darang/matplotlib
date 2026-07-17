import numpy as np
from builder import FigureBuilder
from physics import short_circuit

fig = FigureBuilder(
    title="Why fault current falls off with distance",
    subtitle="Source impedance dominates near the bus; line impedance takes over further out",
    footer="V=13.8kV  Zs=0.8\u03a9  Zline=0.35\u03a9/km  simplified single-source radial model, no c-factor",
)

V_SOURCE_KV = 13.8
Z_SOURCE = 0.8
Z_LINE_PER_KM = 0.35
distances = np.linspace(0, 10, 200)

i_fault = short_circuit.fault_current_profile(V_SOURCE_KV, Z_SOURCE,
                                               Z_LINE_PER_KM, distances)

fig.ax_hero.plot(distances, i_fault, color=fig.accent, linewidth=2.5)
fig.ax_hero.fill_between(distances, i_fault, color=fig.accent, alpha=0.08)
fig.ax_hero.set_xlabel("Fault distance from source (km)")
fig.ax_hero.set_ylabel("I_k'' (A)")
fig.ax_hero.set_title("Fault current drops fast as you move down the feeder")
fig.ax_hero.grid(True, alpha=0.4)

i_at_5km = short_circuit.three_phase_fault_current(V_SOURCE_KV, Z_SOURCE,
                                                    Z_LINE_PER_KM, 5.0)
fig.ax_hero.scatter([5], [i_at_5km], color=fig.accent, zorder=5, s=60)
fig.ax_hero.annotate(f"{i_at_5km:,.0f} A @ 5 km", (5, i_at_5km),
                      xytext=(15, 20), textcoords="offset points",
                      color=fig.fg, fontsize=10, fontfamily=fig.font_mono,
                      arrowprops=dict(arrowstyle="->", color=fig.muted))

mask = distances <= 2
fig.ax_side.plot(distances[mask], i_fault[mask], color=fig.series[1], linewidth=2)
fig.ax_side.set_title("Zoom: protection zone (0-2 km)", fontsize=11)
fig.ax_side.set_xlabel("km")
fig.ax_side.grid(True, alpha=0.4)

fig.save("short_circuit_example.png")
fig.close()
