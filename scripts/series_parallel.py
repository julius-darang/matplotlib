"""
series_parallel.py
Series vs parallel resistance: the direction of the equivalent-R bar
tells the whole story — up for series, down for parallel.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics import series_parallel

theme.apply()

# --- inputs ---------------------------------------------------------
R_VALUE = 10                               # all three resistors equal
R_VALUES = [R_VALUE, R_VALUE, R_VALUE]
R_SERIES = series_parallel.series(*R_VALUES)
R_PARALLEL = series_parallel.parallel(*R_VALUES)
R_SINGLE = R_VALUE

labels  = ["R₁", "R₂", "R₃", "Series", "Parallel"]
values  = [*R_VALUES, R_SERIES, R_PARALLEL]
colors  = [theme.MUTED, theme.MUTED, theme.MUTED,
           theme.ACCENT, theme.SERIES[1]]

# --- layout ---------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.25)

ax_main = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# --- main panel: bar chart of individual vs equivalent ---------------
x_pos = np.arange(len(labels))
bars = ax_main.bar(x_pos, values, color=colors, width=0.5, edgecolor=None)

# label each bar with its value on top
for bar, val in zip(bars, values): 
    ax_main.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f"{val:.1f} Ω" if val != int(val) else f"{int(val)} Ω",
                 ha="center", va="bottom", fontsize=9, color=theme.FG,
                 fontfamily=theme.FONT_MONO)

# directional arrows for series (up) and parallel (down)
ax_main.annotate("series  R↑", xy=(3, R_SERIES), xytext=(-50, 5),
                 textcoords="offset points", ha="center", va="bottom",
                 color=theme.ACCENT, fontweight="bold", fontfamily=theme.FONT_SANS)

ax_main.annotate("parallel  R↓", xy=(4, R_PARALLEL), xytext=(0, 30),
                 textcoords="offset points", ha="center", va="top",
                 color=theme.SERIES[1], fontweight="bold", fontfamily=theme.FONT_SANS)

ax_main.set_xticks(x_pos)
ax_main.set_xticklabels(labels)
ax_main.set_ylabel("Resistance (Ω)")
ax_main.set_title("The same three resistors — two different totals")
ax_main.grid(True, alpha=0.4, axis="y")
ax_main.set_axisbelow(True)

# --- side panel: trend as you add more identical resistors -----------
n_vals = np.arange(1, 11)
series_eq = series_parallel.eq_series_n(R_SINGLE, n_vals)
parallel_eq = series_parallel.eq_parallel_n(R_SINGLE, n_vals)

ax_side.plot(n_vals, series_eq, color=theme.ACCENT, linewidth=2.5,
             label="Series", marker="o", markersize=4)
ax_side.plot(n_vals, parallel_eq, color=theme.SERIES[1], linewidth=2.5,
             label="Parallel", marker="s", markersize=4)
ax_side.axhline(R_SINGLE, color=theme.MUTED, linewidth=0.8, linestyle="--")
ax_side.text(9.5, R_SINGLE + 1.2, f"R₁ = {R_VALUE} Ω", fontsize=8, color=theme.MUTED,
             ha="right", fontfamily=theme.FONT_MONO)

static_arrows = []
for n, (s, p) in zip(n_vals, zip(series_eq, parallel_eq)):
    arr = ax_side.annotate("", xy=(n, p), xytext=(n, s),
                     arrowprops=dict(arrowstyle="<->", color=theme.MUTED, lw=0.8))
    static_arrows.append(arr)

ax_side.set_xlabel("Number of resistors (identical)")
ax_side.set_ylabel("Equivalent R (Ω)")
ax_side.set_title("Wider gap with more resistors", fontsize=11)
ax_side.legend(loc="upper left", fontsize=9, labelcolor=theme.FG,
               framealpha=0)
ax_side.grid(True, alpha=0.4)

# --- header / footer ------------------------------------------------
theme.header(fig,
    "Series vs parallel: R goes up or R goes down",
    "Three equal resistors — series multiplies by 3; parallel divides by 3")
theme.footer(fig,
    f"R₁=R₂=R₃={R_VALUE}Ω  "
    f"Rseries={R_SERIES}Ω  Rparallel={R_PARALLEL:.2f}Ω  "
    "ideal resistors, no tolerance or temperature effects",
    handle="code.arts")

fig.savefig("outputs/series_parallel.png", dpi=150)
print("saved series_parallel.png")

# ======================= ANIMATION ======================================
for arr in static_arrows:
    arr.set_visible(False)

n_frames = 100
n_sweep = np.linspace(1, 10, n_frames)

series_sweep = series_parallel.eq_series_n(R_SINGLE, n_sweep)
parallel_sweep = series_parallel.eq_parallel_n(R_SINGLE, n_sweep)

# Animated artists — hero
hero_label = ax_main.text(0.95, 0.05, "", color=theme.FG, fontsize=10,
                          fontfamily=theme.FONT_MONO, ha="right", va="bottom",
                          transform=ax_main.transAxes)

# Animated artists — side
side_dot_s, = ax_side.plot([], [], "o", color=theme.ACCENT, markersize=10,
                            markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
side_dot_p, = ax_side.plot([], [], "s", color=theme.SERIES[1], markersize=10,
                            markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)

side_arrow = ax_side.annotate("", xy=(0, 0), xytext=(0, 0),
                               arrowprops=dict(arrowstyle="<->", color=theme.MUTED, lw=1.3))
side_label = ax_side.text(0.98, 0.95, "", color=theme.FG, fontsize=9,
                          fontfamily=theme.FONT_MONO, ha="right", va="top",
                          transform=ax_side.transAxes)


def update(frame):
    n = n_sweep[frame]
    s_val = series_parallel.eq_series_n(R_SINGLE, n)
    p_val = series_parallel.eq_parallel_n(R_SINGLE, n)

    side_dot_s.set_data([n], [s_val])
    side_dot_p.set_data([n], [p_val])
    side_arrow.xy = (n, p_val)
    side_arrow.set_position((n, s_val))
    side_label.set_text(f"n = {n:.0f}\nSeries: {s_val:.0f} Ω\nParallel: {p_val:.2f} Ω")

    hero_label.set_text(f"n = {n:.0f}")


anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/series_parallel.gif", fps=20)
plt.close(fig)
