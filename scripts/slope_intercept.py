"""
slope_intercept.py — static PNG + animated GIF
Two-panel: Hero isolates slope (m), Side isolates intercept (b).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.slope_intercept import line_y

theme.apply()

# --- parameters ---------------------------------------------------------
X_MIN, X_MAX = 0, 10
x_full = np.linspace(X_MIN, X_MAX, 300)

# Hero: same b, different m
B_HERO = 0
M_MUTED = 0.5
M_ACCENT = 2.0

# Side: same m, different b
M_SIDE = 1.0
B_MUTED = -2.0
B_ACCENT = 2.0

# Full curves
hero_muted = line_y(x_full, M_MUTED, B_HERO)
hero_accent = line_y(x_full, M_ACCENT, B_HERO)
side_muted = line_y(x_full, M_SIDE, B_MUTED)
side_accent = line_y(x_full, M_SIDE, B_ACCENT)

# --- static figure ------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — same b, different m ======================
ax_hero.plot(x_full, hero_muted, color=theme.MUTED, linewidth=2.5, zorder=3)
ax_hero.plot(x_full, hero_accent, color=theme.ACCENT, linewidth=2.5, zorder=3)
ax_hero.fill_between(x_full, hero_muted, hero_accent,
                     color=theme.ACCENT, alpha=0.06)

ax_hero.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_MUTED, B_HERO),
             f"m = {M_MUTED}", color=theme.MUTED, fontsize=11,
             fontfamily=theme.FONT_MONO, ha="left", va="center")
ax_hero.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_ACCENT, B_HERO),
             f"m = {M_ACCENT}", color=theme.ACCENT, fontsize=11,
             fontfamily=theme.FONT_MONO, ha="left", va="center")

y_hero_max = line_y(X_MAX, M_ACCENT, B_HERO)
ax_hero.set_xlim(X_MIN, X_MAX)
ax_hero.set_ylim(line_y(X_MIN, min(M_MUTED, M_ACCENT), B_HERO) - 1,
                 y_hero_max + 2)
ax_hero.set_xlabel("x")
ax_hero.set_ylabel("y")
ax_hero.set_title("Same b — different m isolates tilt", fontsize=11)
ax_hero.grid(True, alpha=0.3)

# ======================= SIDE — same m, different b ======================
ax_side.plot(x_full, side_muted, color=theme.MUTED, linewidth=2.5, zorder=3)
ax_side.plot(x_full, side_accent, color=theme.ACCENT, linewidth=2.5, zorder=3)
ax_side.fill_between(x_full, side_muted, side_accent,
                     color=theme.ACCENT, alpha=0.06)

ax_side.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_SIDE, B_MUTED),
             f"b = {B_MUTED:.0f}", color=theme.MUTED, fontsize=11,
             fontfamily=theme.FONT_MONO, ha="left", va="center")
ax_side.text(X_MAX * 0.72, line_y(X_MAX * 0.72, M_SIDE, B_ACCENT),
             f"b = {B_ACCENT:.0f}", color=theme.ACCENT, fontsize=11,
             fontfamily=theme.FONT_MONO, ha="left", va="center")

y_side_min = line_y(X_MIN, M_SIDE, B_MUTED)
y_side_max = line_y(X_MAX, M_SIDE, B_ACCENT)
ax_side.set_xlim(X_MIN, X_MAX)
ax_side.set_ylim(y_side_min - 1, y_side_max + 1)
ax_side.set_xlabel("x")
ax_side.set_ylabel("y")
ax_side.set_title("Same m — different b isolates shift", fontsize=11)
ax_side.grid(True, alpha=0.3)

# ======================= HEADER / FOOTER ================================
theme.header(fig,
    "Slope–Intercept Form",
    "y = m·x + b  —  m controls tilt · b controls shift")
theme.footer(fig,
    f"Hero: b={B_HERO}, m∈{{{M_MUTED},{M_ACCENT}}}   "
    f"Side: m={M_SIDE}, b∈{{{B_MUTED:.0f},{B_ACCENT:.0f}}}",
    handle="code.arts")

# ======================= SAVE STATIC ====================================
fig.savefig("outputs/slope_intercept.png", dpi=150)
print("saved slope_intercept.png")

# ======================= ANIMATION ======================================
n_frames = 100
x_sweep = np.linspace(X_MIN, X_MAX, n_frames)

hero_muted_sweep = line_y(x_sweep, M_MUTED, B_HERO)
hero_accent_sweep = line_y(x_sweep, M_ACCENT, B_HERO)
side_muted_sweep = line_y(x_sweep, M_SIDE, B_MUTED)
side_accent_sweep = line_y(x_sweep, M_SIDE, B_ACCENT)

# Animated artists — hero
hero_dot_muted, = ax_hero.plot([], [], "o", color=theme.MUTED, markersize=10,
                                markeredgecolor=theme.FG, markeredgewidth=1.5,
                                zorder=10)
hero_dot_accent, = ax_hero.plot([], [], "o", color=theme.ACCENT, markersize=10,
                                 markeredgecolor=theme.FG, markeredgewidth=1.5,
                                 zorder=10)
hero_vline, = ax_hero.plot([], [], color=theme.MUTED, linewidth=1,
                           linestyle="--", alpha=0.4)
hero_label = ax_hero.text(0.05, 0.95, "", color=theme.FG, fontsize=10,
                          fontfamily=theme.FONT_MONO, ha="left", va="top",
                          transform=ax_hero.transAxes)

# Animated artists — side
side_dot_muted, = ax_side.plot([], [], "o", color=theme.MUTED, markersize=10,
                                markeredgecolor=theme.FG, markeredgewidth=1.5,
                                zorder=10)
side_dot_accent, = ax_side.plot([], [], "o", color=theme.ACCENT, markersize=10,
                                 markeredgecolor=theme.FG, markeredgewidth=1.5,
                                 zorder=10)
side_vline, = ax_side.plot([], [], color=theme.MUTED, linewidth=1,
                           linestyle="--", alpha=0.4)
side_label = ax_side.text(0.05, 0.95, "", color=theme.FG, fontsize=10,
                          fontfamily=theme.FONT_MONO, ha="left", va="top",
                          transform=ax_side.transAxes)


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


anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/slope_intercept.gif", fps=20)
plt.close(fig)
