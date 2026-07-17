import numpy as np
from builder import FigureBuilder
from physics.slope_intercept import line_y

fig = FigureBuilder(
    title="Slope\u2013Intercept Form",
    subtitle="y = m\u00b7x + b  \u2014  m controls tilt \u00b7 b controls shift",
    footer="Hero: b=0, m\u2208{0.5,2.0}   Side: m=1.0, b\u2208{-2,2}",
)

X_MIN, X_MAX = 0, 10
x_full = np.linspace(X_MIN, X_MAX, 300)

B_HERO = 0
M_MUTED = 0.5
M_ACCENT = 2.0

M_SIDE = 1.0
B_MUTED = -2.0
B_ACCENT = 2.0

hero_muted = line_y(x_full, M_MUTED, B_HERO)
hero_accent = line_y(x_full, M_ACCENT, B_HERO)
side_muted = line_y(x_full, M_SIDE, B_MUTED)
side_accent = line_y(x_full, M_SIDE, B_ACCENT)

fig.ax_hero.plot(x_full, hero_muted, color=fig.muted, linewidth=2.5, zorder=3)
fig.ax_hero.plot(x_full, hero_accent, color=fig.accent, linewidth=2.5, zorder=3)
fig.ax_hero.fill_between(x_full, hero_muted, hero_accent,
                         color=fig.accent, alpha=0.06)

fig.ax_hero.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_MUTED, B_HERO),
                 f"m = {M_MUTED}", color=fig.muted, fontsize=11,
                 fontfamily=fig.font_mono, ha="left", va="center")
fig.ax_hero.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_ACCENT, B_HERO),
                 f"m = {M_ACCENT}", color=fig.accent, fontsize=11,
                 fontfamily=fig.font_mono, ha="left", va="center")

y_hero_max = line_y(X_MAX, M_ACCENT, B_HERO)
fig.ax_hero.set_xlim(X_MIN, X_MAX)
fig.ax_hero.set_ylim(line_y(X_MIN, min(M_MUTED, M_ACCENT), B_HERO) - 1,
                     y_hero_max + 2)
fig.ax_hero.set_xlabel("x")
fig.ax_hero.set_ylabel("y")
fig.ax_hero.set_title("Same b \u2014 different m isolates tilt", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

fig.ax_side.plot(x_full, side_muted, color=fig.muted, linewidth=2.5, zorder=3)
fig.ax_side.plot(x_full, side_accent, color=fig.accent, linewidth=2.5, zorder=3)
fig.ax_side.fill_between(x_full, side_muted, side_accent,
                         color=fig.accent, alpha=0.06)

fig.ax_side.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_SIDE, B_MUTED),
                 f"b = {B_MUTED:.0f}", color=fig.muted, fontsize=11,
                 fontfamily=fig.font_mono, ha="left", va="center")
fig.ax_side.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_SIDE, B_ACCENT),
                 f"b = {B_ACCENT:.0f}", color=fig.accent, fontsize=11,
                 fontfamily=fig.font_mono, ha="left", va="center")

y_side_min = line_y(X_MIN, M_SIDE, B_MUTED)
y_side_max = line_y(X_MAX, M_SIDE, B_ACCENT)
fig.ax_side.set_xlim(X_MIN, X_MAX)
fig.ax_side.set_ylim(y_side_min - 1, y_side_max + 1)
fig.ax_side.set_xlabel("x")
fig.ax_side.set_ylabel("y")
fig.ax_side.set_title("Same m \u2014 different b isolates shift", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

fig.save("slope_intercept.png")

n_frames = 100
x_sweep = np.linspace(X_MIN, X_MAX, n_frames)

hero_muted_sweep = line_y(x_sweep, M_MUTED, B_HERO)
hero_accent_sweep = line_y(x_sweep, M_ACCENT, B_HERO)
side_muted_sweep = line_y(x_sweep, M_SIDE, B_MUTED)
side_accent_sweep = line_y(x_sweep, M_SIDE, B_ACCENT)

hero_dot_muted, = fig.ax_hero.plot([], [], "o", color=fig.muted, markersize=10,
                                   markeredgecolor=fig.fg, markeredgewidth=1.5,
                                   zorder=10)
hero_dot_accent, = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                                    markeredgecolor=fig.fg, markeredgewidth=1.5,
                                    zorder=10)
hero_vline, = fig.ax_hero.plot([], [], color=fig.muted, linewidth=1,
                               linestyle="--", alpha=0.4)
hero_label = fig.ax_hero.text(0.05, 0.95, "", color=fig.fg, fontsize=10,
                              fontfamily=fig.font_mono, ha="left", va="top",
                              transform=fig.ax_hero.transAxes)

side_dot_muted, = fig.ax_side.plot([], [], "o", color=fig.muted, markersize=10,
                                   markeredgecolor=fig.fg, markeredgewidth=1.5,
                                   zorder=10)
side_dot_accent, = fig.ax_side.plot([], [], "o", color=fig.accent, markersize=10,
                                    markeredgecolor=fig.fg, markeredgewidth=1.5,
                                    zorder=10)
side_vline, = fig.ax_side.plot([], [], color=fig.muted, linewidth=1,
                               linestyle="--", alpha=0.4)
side_label = fig.ax_side.text(0.05, 0.95, "", color=fig.fg, fontsize=10,
                              fontfamily=fig.font_mono, ha="left", va="top",
                              transform=fig.ax_side.transAxes)


def update(frame):
    x = x_sweep[frame]
    hy_m = hero_muted_sweep[frame]
    hy_a = hero_accent_sweep[frame]
    sy_m = side_muted_sweep[frame]
    sy_a = side_accent_sweep[frame]

    hero_dot_muted.set_data([x], [hy_m])
    hero_dot_accent.set_data([x], [hy_a])
    hero_vline.set_data([x, x], [min(hy_m, hy_a), max(hy_m, hy_a)])
    hero_label.set_text(f"x = {x:.1f}")

    side_dot_muted.set_data([x], [sy_m])
    side_dot_accent.set_data([x], [sy_a])
    side_vline.set_data([x, x], [min(sy_m, sy_a), max(sy_m, sy_a)])
    side_label.set_text(f"x = {x:.1f}")


fig.animate(n_frames, update, "slope_intercept.gif", fps=20)
