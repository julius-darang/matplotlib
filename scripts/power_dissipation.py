"""
power_dissipation.py — static PNG + animated GIF
Single panel: I (linear) vs P = I²R (quadratic) — the gap is the lesson.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.power_dissipation import power

theme.apply()

# --- parameters ---------------------------------------------------------
R = 10.0           # ohms
I_MAX = 10.0       # maximum current (A)
I_OP = 6.0         # static operating point

# --- data ---------------------------------------------------------------
i_full = np.linspace(0, I_MAX, 300)
p_full = power(i_full, R)

n_frames = 100
i_sweep = np.linspace(0, I_MAX, n_frames)
p_sweep = power(i_sweep, R)

# --- figure -------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 1, figure=fig, left=0.08, right=0.97, top=0.82, bottom=0.14)
ax = fig.add_subplot(gs[0, 0])

# ======================= SINGLE PANEL ==================================
# --- traces ---
ax.plot(i_full, i_full, color=theme.MUTED, linewidth=2, alpha=0.7,
        label="I (linear reference)")
ax.plot(i_full, p_full, color=theme.ACCENT, linewidth=2.5, zorder=3,
        label="P = I²R")

# shaded gap between the two traces
ax.fill_between(i_full, i_full, p_full, color=theme.ACCENT, alpha=0.08)

# static operating point markers
static_dot_linear = ax.scatter([I_OP], [I_OP],
                                color=theme.MUTED, zorder=5, s=60)
static_dot_power = ax.scatter([I_OP], [power(I_OP, R)],
                               color=theme.ACCENT, zorder=5, s=60)
static_vline = ax.axvline(I_OP, color=theme.MUTED,
                           linestyle="--", linewidth=1.2, alpha=0.5)

static_ann = ax.annotate(
    f"I = {I_OP:.1f} A    P = {power(I_OP, R):.0f} W",
    (I_OP, power(I_OP, R)), xytext=(25, -35),
    textcoords="offset points", color=theme.FG, fontsize=10,
    fontfamily=theme.FONT_MONO,
    arrowprops=dict(arrowstyle="->", color=theme.MUTED))

ax.set_xlim(0, I_MAX)
ax.set_ylim(0, max(p_full) * 1.15)
ax.set_xlabel("Current (A)")
ax.set_ylabel("Value")
ax.set_title("Power scales with the square", fontsize=11)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", fontsize=10)

# ======================= HEADER / FOOTER ================================
theme.header(fig,
    "Power Dissipation",
    "The growing gap between I (linear) and P = I²R (quadratic) — "
    "power scales with the square")
theme.footer(fig,
    f"R = {R} Ω    I_max = {I_MAX} A",
    handle="code.arts")

# ======================= SAVE STATIC ====================================
fig.savefig("outputs/power_dissipation.png", dpi=150)
print("saved power_dissipation.png")

# ======================= ANIMATION ======================================
# hide static markers
static_dot_linear.set_visible(False)
static_dot_power.set_visible(False)
static_vline.set_visible(False)
static_ann.set_visible(False)
static_ann.arrow_patch.set_visible(False)

# animated artists
linear_dot, = ax.plot([], [], "o", color=theme.MUTED, markersize=10,
                       markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
power_dot, = ax.plot([], [], "o", color=theme.ACCENT, markersize=10,
                      markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
vline, = ax.plot([], [], color=theme.ACCENT, linewidth=1,
                  linestyle="--", alpha=0.4)
label = ax.text(0.95, 0.95, "", color=theme.FG, fontsize=10,
                fontfamily=theme.FONT_MONO, ha="right", va="top",
                transform=ax.transAxes)


def update(frame):
    i = i_sweep[frame]
    p = p_sweep[frame]

    linear_dot.set_data([i], [i])
    power_dot.set_data([i], [p])
    vline.set_data([i, i], [0, p])
    label.set_text(f"I = {i:.2f} A    P = {p:.0f} W")


anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/power_dissipation.gif", fps=20)
plt.close(fig)
