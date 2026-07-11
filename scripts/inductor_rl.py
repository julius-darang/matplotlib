import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.inductor import i_buildup, i_decay, time_constant

theme.apply()

# --- circuit parameters ---------------------------------------------------
V_SOURCE = 5.0
R = 1            # ohms
L = 2            # henries
TAU = time_constant(R, L)   # 2.0 s

# --- time axis ------------------------------------------------------------
t_max = 5 * TAU
t_full = np.linspace(0, t_max, 300)

n_frames = 100
t_sweep = np.linspace(0, t_max, n_frames)

i_max = V_SOURCE / R

buildup_full = i_buildup(t_full, V_SOURCE, R, TAU)
decay_full   = i_decay(t_full, i_max, TAU)
buildup_anim = i_buildup(t_sweep, V_SOURCE, R, TAU)
decay_anim   = i_decay(t_sweep, i_max, TAU)

# --- figure ---------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — Buildup ===================================
ax_hero.plot(t_full, buildup_full, color=theme.ACCENT, linewidth=2.5, zorder=3)
ax_hero.fill_between(t_full, buildup_full, color=theme.ACCENT, alpha=0.08)

# τ vertical dashed line
ax_hero.axvline(TAU, color=theme.MUTED, linestyle="--", linewidth=1.2, alpha=0.7)
ax_hero.text(TAU, i_max * -0.08, "τ", color=theme.MUTED,
             fontsize=11, fontfamily=theme.FONT_MONO, ha="center", va="top")

# 63 % horizontal line
i_63 = i_max * (1 - np.exp(-1))
ax_hero.axhline(i_63, color=theme.MUTED, linestyle=":", linewidth=1, alpha=0.5)
ax_hero.text(t_max * 0.02, i_63, "  63 %", color=theme.MUTED, fontsize=9,
             fontfamily=theme.FONT_MONO, va="bottom")

ax_hero.set_xlim(0, t_max)
ax_hero.set_ylim(0, i_max * 1.15)
ax_hero.set_xlabel("Time (s)")
ax_hero.set_ylabel("I$_{L}$ (A)")
ax_hero.set_title("Buildup: I(t) = (V$_{S}$/R)(1 − e$^{-t/τ}$)", fontsize=11)
ax_hero.grid(True, alpha=0.3)

# animated artists
hero_dot,   = ax_hero.plot([], [], "o", color=theme.ACCENT, markersize=10,
                            markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
hero_vline, = ax_hero.plot([], [], color=theme.ACCENT, linewidth=1,
                            linestyle="--", alpha=0.4)
hero_label  = ax_hero.text(0.95, 0.95, "", color=theme.FG, fontsize=10,
                            fontfamily=theme.FONT_MONO, ha="right", va="top",
                            transform=ax_hero.transAxes)

# ======================= SIDE — Decay =====================================
ax_side.plot(t_full, decay_full, color=theme.SERIES[1], linewidth=2.5, zorder=3)
ax_side.fill_between(t_full, decay_full, color=theme.SERIES[1], alpha=0.08)

# τ vertical dashed line
ax_side.axvline(TAU, color=theme.MUTED, linestyle="--", linewidth=1.2, alpha=0.7)
ax_side.text(TAU, i_max * -0.08, "τ", color=theme.MUTED,
             fontsize=11, fontfamily=theme.FONT_MONO, ha="center", va="top")

# 37 % horizontal line
i_37 = i_max * np.exp(-1)
ax_side.axhline(i_37, color=theme.MUTED, linestyle=":", linewidth=1, alpha=0.5)
ax_side.text(t_max * 0.02, i_37, "  37 %", color=theme.MUTED, fontsize=9,
             fontfamily=theme.FONT_MONO, va="bottom")

ax_side.set_xlim(0, t_max)
ax_side.set_ylim(0, i_max * 1.15)
ax_side.set_xlabel("Time (s)")
ax_side.set_ylabel("I$_{L}$ (A)")
ax_side.set_title("Decay: I(t) = (V$_{S}$/R) e$^{-t/τ}$", fontsize=11)
ax_side.grid(True, alpha=0.3)

# animated artists
side_dot,   = ax_side.plot([], [], "o", color=theme.SERIES[1], markersize=10,
                            markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
side_vline, = ax_side.plot([], [], color=theme.SERIES[1], linewidth=1,
                            linestyle="--", alpha=0.4)
side_label  = ax_side.text(0.95, 0.95, "", color=theme.FG, fontsize=10,
                            fontfamily=theme.FONT_MONO, ha="right", va="top",
                            transform=ax_side.transAxes)

# ======================= HEADER / FOOTER ==================================
theme.header(fig,
    "RL Time Constant",
    "Current buildup and decay — the same τ = L/R governs both directions")
theme.footer(fig,
    f"V$_{{S}}$={V_SOURCE}V  R={R}Ω  L={L}H  "
    f"τ = L/R = {TAU:.2f}s",
    handle="code.arts")

# ======================= ANIMATION ========================================
def update(frame):
    t = t_sweep[frame]
    ib = buildup_anim[frame]
    ide = decay_anim[frame]

    hero_dot.set_data([t], [ib])
    hero_vline.set_data([t, t], [0, ib])
    hero_label.set_text(f"I = {ib:.2f} A")

    side_dot.set_data([t], [ide])
    side_vline.set_data([t, t], [0, ide])
    side_label.set_text(f"I = {ide:.2f} A")

anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/inductor_rl.gif", fps=20)
plt.close(fig)
