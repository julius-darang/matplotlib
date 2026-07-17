import numpy as np
from builder import FigureBuilder
from physics.phase_1 import series_parallel

fig = FigureBuilder(
    title="Series vs parallel: R goes up or R goes down",
    subtitle="Three equal resistors \u2014 series multiplies by 3; parallel divides by 3",
    footer="R\u2081=R\u2082=R\u2083=10\u03a9  Rseries=30\u03a9  Rparallel=3.33\u03a9  ideal resistors, no tolerance or temperature effects",
)

R_VALUE = 10
R_VALUES = [R_VALUE, R_VALUE, R_VALUE]
R_SERIES = series_parallel.series(*R_VALUES)
R_PARALLEL = series_parallel.parallel(*R_VALUES)

labels  = ["R\u2081", "R\u2082", "R\u2083", "Series", "Parallel"]
values  = [*R_VALUES, R_SERIES, R_PARALLEL]
colors  = [fig.muted, fig.muted, fig.muted, fig.accent, fig.series[1]]

x_pos = np.arange(len(labels))
bars = fig.ax_hero.bar(x_pos, values, color=colors, width=0.5, edgecolor=None)

for bar, val in zip(bars, values):
    fig.ax_hero.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     f"{val:.1f} \u03a9" if val != int(val) else f"{int(val)} \u03a9",
                     ha="center", va="bottom", fontsize=9, color=fig.fg,
                     fontfamily=fig.font_mono)

fig.ax_hero.annotate("series  R\u2191", xy=(3, R_SERIES), xytext=(-50, 5),
                     textcoords="offset points", ha="center", va="bottom",
                     color=fig.accent, fontweight="bold", fontfamily=fig.font_sans)

fig.ax_hero.annotate("parallel  R\u2193", xy=(4, R_PARALLEL), xytext=(0, 30),
                     textcoords="offset points", ha="center", va="top",
                     color=fig.series[1], fontweight="bold", fontfamily=fig.font_sans)

fig.ax_hero.set_xticks(x_pos)
fig.ax_hero.set_xticklabels(labels)
fig.ax_hero.set_ylabel("Resistance (\u03a9)")
fig.ax_hero.set_title("The same three resistors \u2014 two different totals")
fig.ax_hero.grid(True, alpha=0.4, axis="y")
fig.ax_hero.set_axisbelow(True)

n_vals = np.arange(1, 11)
series_eq = series_parallel.eq_series_n(R_VALUE, n_vals)
parallel_eq = series_parallel.eq_parallel_n(R_VALUE, n_vals)

fig.ax_side.plot(n_vals, series_eq, color=fig.accent, linewidth=2.5,
                 label="Series", marker="o", markersize=4)
fig.ax_side.plot(n_vals, parallel_eq, color=fig.series[1], linewidth=2.5,
                 label="Parallel", marker="s", markersize=4)
fig.ax_side.axhline(R_VALUE, color=fig.muted, linewidth=0.8, linestyle="--")
fig.ax_side.text(9.5, R_VALUE + 1.2, f"R\u2081 = {R_VALUE} \u03a9", fontsize=8,
                 color=fig.muted, ha="right", fontfamily=fig.font_mono)

static_arrows = []
for n, (s, p) in zip(n_vals, zip(series_eq, parallel_eq)):
    arr = fig.ax_side.annotate("", xy=(n, p), xytext=(n, s),
                               arrowprops=dict(arrowstyle="<->", color=fig.muted, lw=0.8))
    static_arrows.append(arr)

fig.ax_side.set_xlabel("Number of resistors (identical)")
fig.ax_side.set_ylabel("Equivalent R (\u03a9)")
fig.ax_side.set_title("Wider gap with more resistors", fontsize=11)
fig.ax_side.legend(loc="upper left", fontsize=9, labelcolor=fig.fg, framealpha=0)
fig.ax_side.grid(True, alpha=0.4)

fig.save("series_parallel.png")

for arr in static_arrows:
    arr.set_visible(False)

n_frames = 100
n_sweep = np.linspace(1, 10, n_frames)

series_sweep = series_parallel.eq_series_n(R_VALUE, n_sweep)
parallel_sweep = series_parallel.eq_parallel_n(R_VALUE, n_sweep)

hero_label = fig.ax_hero.text(0.95, 0.05, "", color=fig.fg, fontsize=10,
                              fontfamily=fig.font_mono, ha="right", va="bottom",
                              transform=fig.ax_hero.transAxes)

side_dot_s, = fig.ax_side.plot([], [], "o", color=fig.accent, markersize=10,
                                markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
side_dot_p, = fig.ax_side.plot([], [], "s", color=fig.series[1], markersize=10,
                                markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)

side_arrow = fig.ax_side.annotate("", xy=(0, 0), xytext=(0, 0),
                                   arrowprops=dict(arrowstyle="<->", color=fig.muted, lw=1.3))
side_label = fig.ax_side.text(0.98, 0.95, "", color=fig.fg, fontsize=9,
                              fontfamily=fig.font_mono, ha="right", va="top",
                              transform=fig.ax_side.transAxes)


def update(frame):
    n = n_sweep[frame]
    s_val = series_parallel.eq_series_n(R_VALUE, n)
    p_val = series_parallel.eq_parallel_n(R_VALUE, n)

    side_dot_s.set_data([n], [s_val])
    side_dot_p.set_data([n], [p_val])
    side_arrow.xy = (n, p_val)
    side_arrow.set_position((n, s_val))
    side_label.set_text(f"n = {n:.0f}\nSeries: {s_val:.0f} \u03a9\nParallel: {p_val:.2f} \u03a9")

    hero_label.set_text(f"n = {n:.0f}")


fig.animate(n_frames, update, "series_parallel.gif", fps=20)
