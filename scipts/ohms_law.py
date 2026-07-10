"""
ohms_law.py — static PNG + animated GIF
Two-panel Ohm's Law: I vs R at fixed V (hyperbola) and I vs V at fixed R (line).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics import ohms_law

theme.apply()

# --- parameters ---------------------------------------------------------
V_FIXED = 120.0
R_HIGHLIGHT = 60.0
R_MIN, R_MAX = 5, 200
V_MAX = 240

# --- static data -------------------------------------------------------
resistances = np.linspace(R_MIN, R_MAX, 300)
voltages = np.linspace(0, V_MAX, 300)

i_hyperbola = ohms_law.current_profile(V_FIXED, resistances)
i_at_r = ohms_law.current(V_FIXED, R_HIGHLIGHT)
p_at_r = ohms_law.power(V_FIXED, R_HIGHLIGHT)
i_linear = voltages / R_HIGHLIGHT

# --- figure --------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.25)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — I vs R ==================================
ax_hero.plot(resistances, i_hyperbola, color=theme.ACCENT, linewidth=2.5)
ax_hero.fill_between(resistances, i_hyperbola, color=theme.ACCENT, alpha=0.08)

ax_hero.set_xlim(R_MIN, R_MAX)
ax_hero.set_ylim(0, i_hyperbola[0] * 1.15)
ax_hero.set_xlabel("Resistance (Ω)")
ax_hero.set_ylabel("Current (A)")
ax_hero.set_title("I = V / R — fixed voltage (120 V)", fontsize=11)
ax_hero.grid(True, alpha=0.3)

static_dot_hero = ax_hero.scatter([R_HIGHLIGHT], [i_at_r],
                                   color=theme.ACCENT, zorder=5, s=60)
static_ann = ax_hero.annotate(
    f"{i_at_r:.2f} A @ {R_HIGHLIGHT:.1f} Ω ({p_at_r:.0f} W)",
    (R_HIGHLIGHT, i_at_r), xytext=(25, 35),
    textcoords="offset points", color=theme.FG, fontsize=10,
    fontfamily=theme.FONT_MONO,
    arrowprops=dict(arrowstyle="->", color=theme.MUTED))

# ======================= SIDE — I vs V ==================================
side_plot, = ax_side.plot(voltages, i_linear, color=theme.SERIES[1], linewidth=2.5)
side_fill = ax_side.fill_between(voltages, i_linear, color=theme.SERIES[1], alpha=0.08)
side_dot_static = ax_side.scatter([V_FIXED], [i_at_r],
                                   color=theme.SERIES[1], zorder=5, s=60)

ax_side.set_xlim(0, V_MAX)
ax_side.set_ylim(0, i_linear[-1] * 1.15)
ax_side.set_xlabel("Voltage (V)")
ax_side.set_ylabel("Current (A)")
ax_side.set_title("I = V / R — linear at fixed R (60 Ω)", fontsize=11)
ax_side.grid(True, alpha=0.3)

# ======================= HEADER / FOOTER ================================
theme.header(fig,
    "Ohm's Law: two ways to see I = V / R",
    "Left: hyperbola at fixed voltage — Right: straight line at fixed resistance")
theme.footer(fig,
    f"V={V_FIXED}V  R={R_HIGHLIGHT:.0f}\u03a9  I={i_at_r:.2f}A  P={p_at_r:.0f}W  "
    "DC resistive circuit, no temperature effects",
    handle="code.arts")

# ======================= SAVE STATIC ====================================
fig.savefig("outputs/ohms_law.png", dpi=150)
print("saved ohms_law.png")

# ======================= ANIMATION ======================================
# Hide static markers for the animation
static_dot_hero.set_visible(False)
static_ann.set_visible(False)
static_ann.arrow_patch.set_visible(False)
side_dot_static.set_visible(False)

# Precompute sweep data
n_frames = 100
r_sweep = np.linspace(R_MIN, R_MAX, n_frames)
i_r_sweep = V_FIXED / r_sweep
p_sweep = V_FIXED ** 2 / r_sweep

v_sweep = np.linspace(0, V_MAX, n_frames)
i_v_sweep = v_sweep / R_HIGHLIGHT

# Animated artists — hero
hero_dot, = ax_hero.plot([], [], "o", color=theme.ACCENT, markersize=10,
                         markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
hero_vline, = ax_hero.plot([], [], color=theme.ACCENT, linewidth=1,
                           linestyle="--", alpha=0.4)
hero_hline, = ax_hero.plot([], [], color=theme.ACCENT, linewidth=1,
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
    r = r_sweep[frame]
    i_r = i_r_sweep[frame]
    p = p_sweep[frame]

    v = v_sweep[frame]
    i_v = i_v_sweep[frame]

    # Hero — sweep R at fixed V
    hero_dot.set_data([r], [i_r])
    hero_vline.set_data([r, r], [0, i_r])
    hero_hline.set_data([R_MIN, r], [i_r, i_r])
    hero_label.set_text(f"R = {r:.1f} \u03a9\nI = {i_r:.2f} A\nP = {p:.0f} W")

    # Side — sweep V at fixed R
    side_dot_anim.set_data([v], [i_v])
    side_vline_anim.set_data([v, v], [0, i_v])
    side_label.set_text(f"V = {v:.1f} V\nI = {i_v:.2f} A")


anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/ohms_law.gif", fps=20)
plt.close(fig)
