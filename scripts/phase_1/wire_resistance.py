import numpy as np
from builder import FigureBuilder
from physics.phase_1.wire_resistance import r_vs_length, r_vs_area

fig = FigureBuilder(
    title="Wire Resistance: R = \u03c1L / A",
    subtitle="Left: linear with length \u2014 Right: inverse with cross-section",
    footer="\u03c1 = 1.68e-08 \u03a9\u00b7m (copper)  L = 50 m  A = 0.5 mm\u00b2  R = 1.68 \u03a9",
)

RHO = 1.68e-8
A_FIXED = 0.5
A_FIXED_M2 = A_FIXED * 1e-6
L_HIGHLIGHT = 50.0
L_MIN, L_MAX = 0, 100
A_MIN, A_MAX = 0.1, 2.0

lengths = np.linspace(L_MIN, L_MAX, 300)
areas_mm2 = np.linspace(A_MIN, A_MAX, 300)

r_length = RHO * lengths / A_FIXED_M2
r_area_at_l = RHO * L_HIGHLIGHT / (areas_mm2 * 1e-6)
r_highlight = RHO * L_HIGHLIGHT / A_FIXED_M2

fig.ax_hero.plot(lengths, r_length, color=fig.accent, linewidth=2.5)
fig.ax_hero.fill_between(lengths, r_length, color=fig.accent, alpha=0.08)

static_dot_hero = fig.ax_hero.scatter([L_HIGHLIGHT], [r_highlight],
                                       color=fig.accent, zorder=5, s=60)
static_ann_hero = fig.ax_hero.annotate(
    f"R = {r_highlight:.2f} \u03a9 @ L = {L_HIGHLIGHT:.0f} m",
    (L_HIGHLIGHT, r_highlight), xytext=(20, 35),
    textcoords="offset points", color=fig.fg, fontsize=10,
    fontfamily=fig.font_mono,
    arrowprops=dict(arrowstyle="->", color=fig.muted))

fig.ax_hero.set_xlim(L_MIN, L_MAX)
fig.ax_hero.set_ylim(0, r_length[-1] * 1.25)
fig.ax_hero.set_xlabel("Length (m)")
fig.ax_hero.set_ylabel("Resistance (\u03a9)")
fig.ax_hero.set_title("R = \u03c1L / A \u2014 at fixed cross-section", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

side_line, = fig.ax_side.plot(areas_mm2, r_area_at_l, color=fig.series[1], linewidth=2.5)
side_fill = fig.ax_side.fill_between(areas_mm2, r_area_at_l,
                                      color=fig.series[1], alpha=0.08)

side_dot_static = fig.ax_side.scatter([A_FIXED], [r_highlight],
                                       color=fig.series[1], zorder=5, s=60)
static_ann_side = fig.ax_side.annotate(
    f"R = {r_highlight:.2f} \u03a9",
    (A_FIXED, r_highlight), xytext=(20, -30),
    textcoords="offset points", color=fig.fg, fontsize=10,
    fontfamily=fig.font_mono,
    arrowprops=dict(arrowstyle="->", color=fig.muted))

fig.ax_side.set_xlim(A_MIN, A_MAX)
fig.ax_side.set_ylim(0, r_area_at_l[0] * 1.25)
fig.ax_side.set_xlabel("Cross-sectional area (mm\u00b2)")
fig.ax_side.set_ylabel("Resistance (\u03a9)")
fig.ax_side.set_title("R = \u03c1L / A \u2014 at fixed length", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

fig.save("wire_resistance.png")

static_dot_hero.set_visible(False)
static_ann_hero.set_visible(False)
static_ann_hero.arrow_patch.set_visible(False)
side_dot_static.set_visible(False)
static_ann_side.set_visible(False)
static_ann_side.arrow_patch.set_visible(False)
side_fill.set_visible(False)

n_frames = 100
l_sweep = np.linspace(L_MIN + 0.5, L_MAX, n_frames)
r_l_sweep = RHO * l_sweep / A_FIXED_M2
a_sweep = np.linspace(A_MIN + 0.05, A_MAX, n_frames)
r_a_sweep = RHO * L_HIGHLIGHT / (a_sweep * 1e-6)

hero_dot, = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                              markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
hero_vline, = fig.ax_hero.plot([], [], color=fig.accent, linewidth=1,
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
    L = l_sweep[frame]
    R_L = r_l_sweep[frame]
    A = a_sweep[frame]
    R_A = r_a_sweep[frame]

    hero_dot.set_data([L], [R_L])
    hero_vline.set_data([L, L], [0, R_L])
    hero_label.set_text(f"L = {L:.1f} m\nR = {R_L:.2f} \u03a9")

    side_dot_anim.set_data([A], [R_A])
    side_vline_anim.set_data([A, A], [0, R_A])
    side_label.set_text(f"A = {A:.2f} mm\u00b2\nR = {R_A:.2f} \u03a9")


fig.animate(n_frames, update, "wire_resistance.gif", fps=20)
