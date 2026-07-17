import numpy as np
from builder import FigureBuilder
from physics.phase_1 import ohms_law

fig = FigureBuilder(
    title="Ohm's Law: two ways to see I = V / R",
    subtitle="Left: hyperbola at fixed voltage \u2014 Right: straight line at fixed resistance",
    footer="V=120V  R=60\u03a9  I=2.00A  P=240W  DC resistive circuit, no temperature effects",
)

V_FIXED = 120.0
R_HIGHLIGHT = 60.0
R_MIN, R_MAX = 5, 200
V_MAX = 240

resistances = np.linspace(R_MIN, R_MAX, 300)
voltages = np.linspace(0, V_MAX, 300)

i_hyperbola = ohms_law.current_profile(V_FIXED, resistances)
i_at_r = ohms_law.current(V_FIXED, R_HIGHLIGHT)
p_at_r = ohms_law.power(V_FIXED, R_HIGHLIGHT)
i_linear = voltages / R_HIGHLIGHT

fig.ax_hero.plot(resistances, i_hyperbola, color=fig.accent, linewidth=2.5)
fig.ax_hero.fill_between(resistances, i_hyperbola, color=fig.accent, alpha=0.08)

fig.ax_hero.set_xlim(R_MIN, R_MAX)
fig.ax_hero.set_ylim(0, i_hyperbola[0] * 1.15)
fig.ax_hero.set_xlabel("Resistance (\u03a9)")
fig.ax_hero.set_ylabel("Current (A)")
fig.ax_hero.set_title("I = V / R \u2014 fixed voltage (120 V)", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

static_dot_hero = fig.ax_hero.scatter([R_HIGHLIGHT], [i_at_r],
                                       color=fig.accent, zorder=5, s=60)
static_ann = fig.ax_hero.annotate(
    f"{i_at_r:.2f} A @ {R_HIGHLIGHT:.1f} \u03a9 ({p_at_r:.0f} W)",
    (R_HIGHLIGHT, i_at_r), xytext=(25, 35),
    textcoords="offset points", color=fig.fg, fontsize=10,
    fontfamily=fig.font_mono,
    arrowprops=dict(arrowstyle="->", color=fig.muted))

side_line, = fig.ax_side.plot(voltages, i_linear, color=fig.series[1], linewidth=2.5)
side_fill = fig.ax_side.fill_between(voltages, i_linear, color=fig.series[1], alpha=0.08)
side_dot_static = fig.ax_side.scatter([V_FIXED], [i_at_r],
                                       color=fig.series[1], zorder=5, s=60)

fig.ax_side.set_xlim(0, V_MAX)
fig.ax_side.set_ylim(0, i_linear[-1] * 1.15)
fig.ax_side.set_xlabel("Voltage (V)")
fig.ax_side.set_ylabel("Current (A)")
fig.ax_side.set_title("I = V / R \u2014 linear at fixed R (60 \u03a9)", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

fig.save("ohms_law.png")

static_dot_hero.set_visible(False)
static_ann.set_visible(False)
static_ann.arrow_patch.set_visible(False)
side_dot_static.set_visible(False)

n_frames = 100
r_sweep = np.linspace(R_MIN, R_MAX, n_frames)
i_r_sweep = V_FIXED / r_sweep
p_sweep = V_FIXED ** 2 / r_sweep
v_sweep = np.linspace(0, V_MAX, n_frames)
i_v_sweep = v_sweep / R_HIGHLIGHT

hero_dot, = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                              markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
hero_vline, = fig.ax_hero.plot([], [], color=fig.accent, linewidth=1,
                                linestyle="--", alpha=0.4)
hero_hline, = fig.ax_hero.plot([], [], color=fig.accent, linewidth=1,
                                linestyle="--", alpha=0.4)
hero_label = fig.ax_hero.text(0.05, 0.95, "", color=fig.fg, fontsize=10,
                              fontfamily=fig.font_mono, ha="left", va="top",
                              transform=fig.ax_hero.transAxes)

side_dot_anim, = fig.ax_side.plot([], [], "o", color=fig.series[1], markersize=10,
                                   markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
side_vline_anim, = fig.ax_side.plot([], [], color=fig.series[1], linewidth=1,
                                     linestyle="--", alpha=0.4)
side_label = fig.ax_side.text(0.05, 0.95, "", color=fig.fg, fontsize=10,
                              fontfamily=fig.font_mono, ha="left", va="top",
                              transform=fig.ax_side.transAxes)


def update(frame):
    r = r_sweep[frame]
    i_r = i_r_sweep[frame]
    p = p_sweep[frame]
    v = v_sweep[frame]
    i_v = i_v_sweep[frame]

    hero_dot.set_data([r], [i_r])
    hero_vline.set_data([r, r], [0, i_r])
    hero_hline.set_data([R_MIN, r], [i_r, i_r])
    hero_label.set_text(f"R = {r:.1f} \u03a9\nI = {i_r:.2f} A\nP = {p:.0f} W")

    side_dot_anim.set_data([v], [i_v])
    side_vline_anim.set_data([v, v], [0, i_v])
    side_label.set_text(f"V = {v:.1f} V\nI = {i_v:.2f} A")


fig.animate(n_frames, update, "ohms_law.gif", fps=20)
