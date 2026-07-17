import numpy as np
from builder import FigureBuilder
from physics.phase_2.rlc import step_response, settling_time, settling_sweep

OMEGA0 = 1.0
ZETA_VALUES = [0.2, 1.0, 2.0]
ZETA_LABELS = ["\u03b6=0.2  underdamped", "\u03b6=1.0  critical", "\u03b6=2.0  overdamped"]
CURVE_COLORS = []
CURVE_STYLES = ["-", "--", "-"]
LABEL_X = [3.3, 4.5, 8.0]
LABEL_XOFF = 0.4

fig = FigureBuilder(
    title="Three dampings, one circuit",
    subtitle="Underdamped rings; critical settles fastest without overshoot; overdamped crawls",
    footer="\u03c9\u2080 = 1 rad/s  V\u209B = 1 V  2% settling band",
)

t_max = 20
t = np.linspace(0, t_max, 2000)
colors = [fig.accent, fig.muted, fig.series[1]]

for zeta, color, ls, label, lx in zip(
    ZETA_VALUES, colors, CURVE_STYLES, ZETA_LABELS, LABEL_X
):
    v = step_response(t, zeta, OMEGA0)
    fig.ax_hero.plot(t, v, color=color, linestyle=ls, linewidth=2.5, zorder=3)
    idx = np.searchsorted(t, lx)
    fig.ax_hero.text(
        t[idx] + LABEL_XOFF, v[idx], label, color=color, fontsize=9,
        fontfamily=fig.font_mono, va="bottom",
    )

fig.ax_hero.axhline(1.0, color=fig.grid, linestyle=":", linewidth=0.8, alpha=0.5)
fig.ax_hero.set_xlim(0, t_max)
fig.ax_hero.set_ylim(-0.1, 1.6)
fig.ax_hero.set_xlabel("Time (s)")
fig.ax_hero.set_ylabel("v$_{C}$ (V)")
fig.ax_hero.set_title("Step response v$_{C}$(t) for three damping ratios", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

zetas, t_settle = settling_sweep(omega0=OMEGA0)
fig.ax_side.plot(zetas, t_settle, color=fig.accent, linewidth=2.5, zorder=3)
fig.ax_side.fill_between(zetas, t_settle, color=fig.accent, alpha=0.08)

for zeta, color in zip(ZETA_VALUES, colors):
    ts = settling_time(zeta, OMEGA0)
    fig.add_event_marker(fig.ax_side, zeta, ts, label=f"\u03b6={zeta}")

fig.ax_side.set_xlim(0, 3.0)
fig.ax_side.set_ylim(0, 30)
fig.ax_side.set_xlabel("Damping ratio \u03b6")
fig.ax_side.set_ylabel("t$_{s}$ (s)")
fig.ax_side.set_title("2% settling time", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

n_frames = 100
t_sweep = np.linspace(0, t_max, n_frames)
v_sweeps = [step_response(t_sweep, z, OMEGA0) for z in ZETA_VALUES]

hero_dots = []
for color in colors:
    dot, = fig.ax_hero.plot(
        [], [], "o", color=color, markersize=10,
        markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10,
    )
    hero_dots.append(dot)

hero_vline, = fig.ax_hero.plot(
    [], [], color=fig.muted, linewidth=1, linestyle="--", alpha=0.4,
)

hero_label = fig.ax_hero.text(
    0.95, 0.95, "", color=fig.fg, fontsize=10,
    fontfamily=fig.font_mono, ha="right", va="top",
    transform=fig.ax_hero.transAxes,
)

fig.save("rlc_step_response.png")


def update(frame):
    t_cur = t_sweep[frame]
    ylo, yhi = fig.ax_hero.get_ylim()
    hero_vline.set_data([t_cur, t_cur], [ylo, yhi])
    for dot, vs in zip(hero_dots, v_sweeps):
        dot.set_data([t_cur], [vs[frame]])
    v0, v1, v2 = (vs[frame] for vs in v_sweeps)
    hero_label.set_text(
        f"t = {t_cur:.1f}s\n"
        f"\u03b6=0.2: {v0:.2f}V\n"
        f"\u03b6=1.0: {v1:.2f}V\n"
        f"\u03b6=2.0: {v2:.2f}V"
    )


fig.animate(n_frames, update, "rlc_step_response.gif", fps=20)
