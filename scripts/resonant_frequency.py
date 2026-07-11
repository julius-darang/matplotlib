import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.resonant_frequency import f0, f0_curve

theme.apply()

# --- circuit parameters ---------------------------------------------------
L = 10e-3            # 10 mH
C_BASE = 1e-6         # 1 µF
F0_BASE = f0(L, C_BASE)   # ≈ 1591.5 Hz

# --- sweep range: C spans roughly a decade around C_BASE ------------------
C_MIN = C_BASE / 3.0
C_MAX = C_BASE * 3.0

n_frames = 100
c_sweep = np.geomspace(C_MIN, C_MAX, n_frames)
f0_sweep = f0_curve(c_sweep, L)

# --- side panel full curve (denser) ---
c_full = np.geomspace(C_MIN, C_MAX, 300)
f0_full = f0_curve(c_full, L)

# --- figure ---------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — Frequency Ruler ==========================
F_MIN, F_MAX = 100, 10000   # Hz, log range covering the sweep

# build a horizontal frequency ruler
ax_hero.spines[:].set_visible(False)
ax_hero.set_xticks([])
ax_hero.set_yticks([])
ax_hero.set_xlim(F_MIN, F_MAX)
ax_hero.set_ylim(-0.5, 5)
ax_hero.set_xscale("log")
ax_hero.set_title("Resonant frequency f₀ = 1 / (2π√LC)", fontsize=11)

# draw the frequency axis line
ax_hero.plot([F_MIN, F_MAX], [0, 0], color=theme.GRID, linewidth=2, zorder=1)

# decade tick marks
for decade_exp in range(int(np.log10(F_MIN)), int(np.log10(F_MAX)) + 1):
    freq = 10 ** decade_exp
    if F_MIN <= freq <= F_MAX:
        ax_hero.plot([freq, freq], [-0.3, 0.3], color=theme.MUTED, linewidth=1.2)
        exp = int(np.log10(freq))
        # ax_hero.text(freq, -0.7, f"$10^{{{exp}}}$", color=theme.MUTED, fontsize=9,
        #              fontfamily=theme.FONT_MONO, ha="center", va="top")

ax_hero.text(F_MAX * 1.1, 0, "f (Hz)", color=theme.MUTED, fontsize=9,
             fontfamily=theme.FONT_MONO, va="center")

# f₀ marker — vertical line + dot
hero_f0_line, = ax_hero.plot([F0_BASE, F0_BASE], [0, 3.5], color=theme.ACCENT,
                             linewidth=2.5, zorder=4)
hero_dot, = ax_hero.plot([F0_BASE], [3.5], "o", color=theme.ACCENT, markersize=14,
                         markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=8)

# readout box (axes coords so it stays put regardless of log scale)
# readout_bg = plt.Rectangle((0.04, 0.54), 0.26, 0.25,
#                             color=theme.BG, ec=theme.GRID, linewidth=0.8,
#                             transform=ax_hero.transAxes, zorder=6)
# ax_hero.add_patch(readout_bg)

readout_text = ax_hero.text(0.07, 0.78, "", color=theme.FG, fontsize=8,
                            fontfamily=theme.FONT_MONO, va="top",
                            transform=ax_hero.transAxes, zorder=7)

# ======================= SIDE — f₀ vs C ==================================
ax_side.plot(c_full * 1e6, f0_full, color=theme.SERIES[1], linewidth=2.5, zorder=3)
ax_side.fill_between(c_full * 1e6, f0_full, color=theme.SERIES[1], alpha=0.08)

ax_side.set_xscale("log")
ax_side.set_yscale("log")
ax_side.set_xlabel("Capacitance (µF)")
ax_side.set_ylabel("f₀ (Hz)")
ax_side.set_title("f₀ ∝ 1 / √C — inverse square root", fontsize=11)
ax_side.grid(True, alpha=0.3)
ax_side.set_xlim(C_MIN * 1e6, C_MAX * 1e6)
ax_side.set_ylim(f0_full[-1] * 0.8, f0_full[0] * 1.2)

# animated artists — side
side_dot, = ax_side.plot([], [], "o", color=theme.ACCENT, markersize=10,
                         markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
side_vline, = ax_side.plot([], [], color=theme.ACCENT, linewidth=1,
                           linestyle="--", alpha=0.4)
side_label = ax_side.text(0.05, 0.95, "", color=theme.FG, fontsize=10,
                          fontfamily=theme.FONT_MONO, ha="left", va="top",
                          transform=ax_side.transAxes)

# ======================= HEADER / FOOTER ==================================
theme.header(fig,
    "Resonant Frequency",
    "f₀ = 1 / (2π√LC) — sweeping C shows the inverse-square-root sensitivity")
theme.footer(fig,
    f"L = {L*1e3:.1f} mH  C = {C_BASE*1e6:.2f} µF  "
    f"f₀ = {F0_BASE:.0f} Hz  ideal LC, no resistance",
    handle="code.arts")

# ======================= ANIMATION ========================================
def update(frame):
    c_curr = c_sweep[frame]
    f0_curr = f0_sweep[frame]

    # Hero — move marker
    hero_f0_line.set_xdata([f0_curr, f0_curr])
    hero_dot.set_xdata([f0_curr])

    # readout
    readout_text.set_text(
        f"   L = {L*1e3:.1f} mH\n"
        f"   C = {c_curr*1e6:.2f} µF\n"
        f"   f₀ = {f0_curr:.0f} Hz"
    )

    # Side — highlight point
    side_dot.set_data([c_curr * 1e6], [f0_curr])
    side_vline.set_data([c_curr * 1e6, c_curr * 1e6],
                        [ax_side.get_ylim()[0], f0_curr])
    side_label.set_text(f"C = {c_curr*1e6:.2f} µF\nf₀ = {f0_curr:.0f} Hz")

anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/resonant_frequency.gif", fps=20)
plt.close(fig)
