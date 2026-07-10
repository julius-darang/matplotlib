import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.capacitor import v_charge, v_discharge, time_constant

theme.apply()

# --- circuit parameters ---------------------------------------------------
V_SOURCE = 5.0
R = 1_000          # ohms
C = 2e-3           # farads
TAU = time_constant(R, C)   # 2.0 s

# --- time axis ------------------------------------------------------------
t_max = 5 * TAU
t_full = np.linspace(0, t_max, 300)

n_frames = 100
t_sweep = np.linspace(0, t_max, n_frames)

charge_full = v_charge(t_full, V_SOURCE, TAU)
disc_full   = v_discharge(t_full, V_SOURCE, TAU)
charge_anim = v_charge(t_sweep, V_SOURCE, TAU)
disc_anim   = v_discharge(t_sweep, V_SOURCE, TAU)

# --- figure ---------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — Charging ==================================
ax_hero.plot(t_full, charge_full, color=theme.ACCENT, linewidth=2.5, zorder=3)
ax_hero.fill_between(t_full, charge_full, color=theme.ACCENT, alpha=0.08)

# τ vertical dashed line
ax_hero.axvline(TAU, color=theme.MUTED, linestyle="--", linewidth=1.2, alpha=0.7)
ax_hero.text(TAU, V_SOURCE * -0.08, "τ", color=theme.MUTED,
             fontsize=11, fontfamily=theme.FONT_MONO, ha="center", va="top")

# 63 % horizontal line
v_63 = V_SOURCE * (1 - np.exp(-1))
ax_hero.axhline(v_63, color=theme.MUTED, linestyle=":", linewidth=1, alpha=0.5)
ax_hero.text(t_max * 0.02, v_63, "  63 %", color=theme.MUTED, fontsize=9,
             fontfamily=theme.FONT_MONO, va="bottom")

ax_hero.set_xlim(0, t_max)
ax_hero.set_ylim(0, V_SOURCE * 1.15)
ax_hero.set_xlabel("Time (s)")
ax_hero.set_ylabel("V$_{C}$ (V)")
ax_hero.set_title("Charging: V(t) = V$_{S}$(1 − e$^{-t/τ}$)", fontsize=11)
ax_hero.grid(True, alpha=0.3)

# animated artists
hero_dot,   = ax_hero.plot([], [], "o", color=theme.ACCENT, markersize=10,
                            markeredgecolor=theme.FG, markeredgewidth=1.5, zorder=10)
hero_vline, = ax_hero.plot([], [], color=theme.ACCENT, linewidth=1,
                            linestyle="--", alpha=0.4)
hero_label  = ax_hero.text(0.95, 0.95, "", color=theme.FG, fontsize=10,
                            fontfamily=theme.FONT_MONO, ha="right", va="top",
                            transform=ax_hero.transAxes)

# ======================= SIDE — Discharging ===============================
ax_side.plot(t_full, disc_full, color=theme.SERIES[1], linewidth=2.5, zorder=3)
ax_side.fill_between(t_full, disc_full, color=theme.SERIES[1], alpha=0.08)

# τ vertical dashed line
ax_side.axvline(TAU, color=theme.MUTED, linestyle="--", linewidth=1.2, alpha=0.7)
ax_side.text(TAU, V_SOURCE * -0.08, "τ", color=theme.MUTED,
             fontsize=11, fontfamily=theme.FONT_MONO, ha="center", va="top")

# 37 % horizontal line
v_37 = V_SOURCE * np.exp(-1)
ax_side.axhline(v_37, color=theme.MUTED, linestyle=":", linewidth=1, alpha=0.5)
ax_side.text(t_max * 0.02, v_37, "  37 %", color=theme.MUTED, fontsize=9,
             fontfamily=theme.FONT_MONO, va="bottom")

ax_side.set_xlim(0, t_max)
ax_side.set_ylim(0, V_SOURCE * 1.15)
ax_side.set_xlabel("Time (s)")
ax_side.set_ylabel("V$_{C}$ (V)")
ax_side.set_title("Discharging: V(t) = V$_{S}$ e$^{-t/τ}$", fontsize=11)
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
    "RC Time Constant",
    "Charge and discharge — the same τ = RC governs both directions")
theme.footer(fig,
    f"V$_{{S}}$={V_SOURCE}V  R={R/1000:.0f}kΩ  C={C*1e6:.0f}μF  "
    f"τ = RC = {TAU:.2f}s",
    handle="code.arts")

# ======================= ANIMATION ========================================
def update(frame):
    t = t_sweep[frame]
    vc = charge_anim[frame]
    vd = disc_anim[frame]

    hero_dot.set_data([t], [vc])
    hero_vline.set_data([t, t], [0, vc])
    hero_label.set_text(f"V = {vc:.2f} V")

    side_dot.set_data([t], [vd])
    side_vline.set_data([t, t], [0, vd])
    side_label.set_text(f"V = {vd:.2f} V")

anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/capacitor_rc.gif", fps=20)
plt.close(fig)
