"""
wire_resistance.py — static PNG + animated GIF
Two-panel: R vs length (linear) and R vs cross-sectional area (inverse) for a copper wire.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.wire_resistance import r_vs_length, r_vs_area

theme.apply()

# --- material & geometry ------------------------------------------------
RHO = 1.68e-8        # Ω·m (copper at 20°C)
A_FIXED = 0.5         # mm² (cross-section for hero panel)
A_FIXED_M2 = A_FIXED * 1e-6
L_HIGHLIGHT = 50.0    # m (length for side panel)
L_MIN, L_MAX = 0, 100
A_MIN, A_MAX = 0.1, 2.0  # mm²

# --- static data --------------------------------------------------------
lengths = np.linspace(L_MIN, L_MAX, 300)
areas_mm2 = np.linspace(A_MIN, A_MAX, 300)

r_length = RHO * lengths / A_FIXED_M2
r_area_at_l = RHO * L_HIGHLIGHT / (areas_mm2 * 1e-6)

r_highlight = RHO * L_HIGHLIGHT / A_FIXED_M2

# --- figure -------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.25)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — R vs L ==================================
ax_hero.plot(lengths, r_length, color=theme.ACCENT, linewidth=2.5)
ax_hero.fill_between(lengths, r_length, color=theme.ACCENT, alpha=0.08)

static_dot_hero = ax_hero.scatter([L_HIGHLIGHT], [r_highlight],
                                   color=theme.ACCENT, zorder=5, s=60)
static_ann_hero = ax_hero.annotate(
    f"R = {r_highlight:.2f} Ω @ L = {L_HIGHLIGHT:.0f} m",
    (L_HIGHLIGHT, r_highlight), xytext=(20, 35),
    textcoords="offset points", color=theme.FG, fontsize=10,
    fontfamily=theme.FONT_MONO,
    arrowprops=dict(arrowstyle="->", color=theme.MUTED))

ax_hero.set_xlim(L_MIN, L_MAX)
ax_hero.set_ylim(0, r_length[-1] * 1.25)
ax_hero.set_xlabel("Length (m)")
ax_hero.set_ylabel("Resistance (Ω)")
ax_hero.set_title("R = ρL / A — at fixed cross-section", fontsize=11)
ax_hero.grid(True, alpha=0.3)

# ======================= SIDE — R vs A ==================================
side_line, = ax_side.plot(areas_mm2, r_area_at_l, color=theme.SERIES[1],
                           linewidth=2.5)
side_fill = ax_side.fill_between(areas_mm2, r_area_at_l,
                                  color=theme.SERIES[1], alpha=0.08)

side_dot_static = ax_side.scatter([A_FIXED], [r_highlight],
                                   color=theme.SERIES[1], zorder=5, s=60)
static_ann_side = ax_side.annotate(
    f"R = {r_highlight:.2f} Ω",
    (A_FIXED, r_highlight), xytext=(20, -30),
    textcoords="offset points", color=theme.FG, fontsize=10,
    fontfamily=theme.FONT_MONO,
    arrowprops=dict(arrowstyle="->", color=theme.MUTED))

ax_side.set_xlim(A_MIN, A_MAX)
ax_side.set_ylim(0, r_area_at_l[0] * 1.25)
ax_side.set_xlabel("Cross-sectional area (mm²)")
ax_side.set_ylabel("Resistance (Ω)")
ax_side.set_title("R = ρL / A — at fixed length", fontsize=11)
ax_side.grid(True, alpha=0.3)

# ======================= HEADER / FOOTER ================================
theme.header(fig,
    "Wire Resistance: R = ρL / A",
    "Left: linear with length — Right: inverse with cross-section")
theme.footer(fig,
    f"ρ = {RHO:.2e} Ω·m (copper)  L = {L_HIGHLIGHT:.0f} m  "
    f"A = {A_FIXED:.1f} mm²  R = {r_highlight:.2f} Ω",
    handle="code.arts")

# ======================= SAVE STATIC ====================================
fig.savefig("outputs/wire_resistance.png", dpi=150)
print("saved wire_resistance.png")

# ======================= ANIMATION ======================================
# hide static markers
static_dot_hero.set_visible(False)
static_ann_hero.set_visible(False)
static_ann_hero.arrow_patch.set_visible(False)
side_dot_static.set_visible(False)
static_ann_side.set_visible(False)
static_ann_side.arrow_patch.set_visible(False)
side_fill.set_visible(False)

# Precompute sweep data
n_frames = 100
l_sweep = np.linspace(L_MIN + 0.5, L_MAX, n_frames)
r_l_sweep = RHO * l_sweep / A_FIXED_M2

a_sweep = np.linspace(A_MIN + 0.05, A_MAX, n_frames)
r_a_sweep = RHO * L_HIGHLIGHT / (a_sweep * 1e-6)

# Animated artists — hero
hero_dot, = ax_hero.plot([], [], "o", color=theme.ACCENT, markersize=10,
                          markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
hero_vline, = ax_hero.plot([], [], color=theme.ACCENT, linewidth=1,
                            linestyle="--", alpha=0.4)
hero_label = ax_hero.text(0.05, 0.95, "", color=theme.FG, fontsize=10,
                           fontfamily=theme.FONT_MONO, ha="left", va="top",
                           transform=ax_hero.transAxes)

# Animated artists — side
side_dot_anim, = ax_side.plot([], [], "o", color=theme.SERIES[1], markersize=10,
                               markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
side_vline_anim, = ax_side.plot([], [], color=theme.SERIES[1], linewidth=1,
                                 linestyle="--", alpha=0.4)
side_label = ax_side.text(0.05, 0.95, "", color=theme.FG, fontsize=10,
                           fontfamily=theme.FONT_MONO, ha="left", va="top",
                           transform=ax_side.transAxes)


def update(frame):
    L = l_sweep[frame]
    R_L = r_l_sweep[frame]
    A = a_sweep[frame]
    R_A = r_a_sweep[frame]

    hero_dot.set_data([L], [R_L])
    hero_vline.set_data([L, L], [0, R_L])
    hero_label.set_text(f"L = {L:.1f} m\nR = {R_L:.2f} Ω")

    side_dot_anim.set_data([A], [R_A])
    side_vline_anim.set_data([A, A], [0, R_A])
    side_label.set_text(f"A = {A:.2f} mm²\nR = {R_A:.2f} Ω")


anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/wire_resistance.gif", fps=20)
plt.close(fig)
