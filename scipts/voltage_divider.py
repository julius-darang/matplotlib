import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif
from physics.voltage_divider import vout

theme.apply()

VIN = 12.0
R1 = 1_000
R2_MAX = 10_000

n_ramp = 80
r2_forward = np.linspace(0, R2_MAX, n_ramp)
r2_backward = np.linspace(R2_MAX, 0, n_ramp)
r2_sweep = np.concatenate([r2_forward, r2_backward])
n_frames = len(r2_sweep)

vout_values = vout(VIN, R1, r2_sweep)

fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO PANEL =======================
ax_hero.spines[:].set_visible(False)
ax_hero.set_xticks([])
ax_hero.set_yticks([])
ax_hero.set_xlim(-1.2, 3.5)
ax_hero.set_ylim(-1.0, VIN + 1.5)
ax_hero.set_title("V$_{total}$ split by R$_1$ and R$_2$", fontsize=12)

VOLTS = [0.0, 3.0, 6.0, 9.0, 12.0]
VSTR = ["0", "3V", "6V", "9V", "V$_{in}$"]
for v, s in zip(VOLTS, VSTR):
    ax_hero.plot([-0.06, 0], [v, v], color=theme.MUTED, linewidth=0.8)
    ax_hero.text(-0.22, v, s, color=theme.MUTED, fontsize=9,
                 fontfamily=theme.FONT_MONO, va="center", ha="right")

ax_hero.plot([0, 0], [0, VIN], color=theme.GRID, linewidth=3, zorder=1)

top_fill = plt.Rectangle((-0.06, vout_values[0]), 0.12, VIN - vout_values[0],
                          color=theme.MUTED, alpha=0.06, zorder=2)
ax_hero.add_patch(top_fill)

bot_fill = plt.Rectangle((-0.06, 0), 0.12, vout_values[0],
                          color=theme.ACCENT, alpha=0.12, zorder=2)
ax_hero.add_patch(bot_fill)

rail_hl, = ax_hero.plot([0, 0], [0, vout_values[0]], color=theme.ACCENT,
                        linewidth=3, solid_capstyle="round", zorder=3)

marker, = ax_hero.plot([0], [vout_values[0]], "o", color=theme.ACCENT,
                       markersize=14, markeredgecolor=theme.FG,
                       markeredgewidth=1.5, zorder=10)

prev_tick, = ax_hero.plot([-0.08, 0.08], [vout_values[0], vout_values[0]],
                          color=theme.MUTED, linewidth=1.5, alpha=0.35, zorder=5)

vout_text = ax_hero.text(0.3, vout_values[0], f"V$_{{out}}$ = {vout_values[0]:.2f} V",
                         color=theme.FG, fontsize=11, fontfamily=theme.FONT_MONO,
                         va="center")

anno_line, = ax_hero.plot([0.06, 0.25], [vout_values[0], vout_values[0]],
                          color=theme.MUTED, linewidth=0.8, alpha=0.6, zorder=4)

r1_comp = ax_hero.text(0.3, (VIN + vout_values[0]) / 2,
                        f"R$_1$ = {R1/1000:.1f} kΩ",
                        color=theme.MUTED, fontsize=10, fontfamily=theme.FONT_MONO,
                        va="center")

r2_comp = ax_hero.text(0.3, vout_values[0] / 2,
                        f"R$_2$ = {r2_sweep[0]/1000:.2f} kΩ",
                        color=theme.ACCENT, fontsize=10, fontfamily=theme.FONT_MONO,
                        va="center")

vr1_text = ax_hero.text(-0.15, (VIN + vout_values[0]) / 2,
                         f"{VIN - vout_values[0]:.1f}V",
                         color=theme.MUTED, fontsize=8, fontfamily=theme.FONT_MONO,
                         va="center", ha="right")

vr2_text = ax_hero.text(-0.15, vout_values[0] / 2,
                         f"{vout_values[0]:.1f}V",
                         color=theme.ACCENT, fontsize=8, fontfamily=theme.FONT_MONO,
                         va="center", ha="right")

ax_hero.plot([-0.04, 0.04], [VIN, VIN], color=theme.GRID, linewidth=1.5)

ax_hero.text(0, VIN + 0.5, "V$_{total}$", color=theme.MUTED, fontsize=10,
             fontfamily=theme.FONT_SANS, ha="center", va="bottom")

# ======================= SIDE PANEL =======================
r2_full = np.linspace(0, R2_MAX, 200)
vout_full = vout(VIN, R1, r2_full)

ax_side.plot(r2_full / 1000, vout_full, color=theme.SERIES[1], linewidth=2.5,
             zorder=1)
ax_side.fill_between(r2_full / 1000, vout_full, color=theme.SERIES[1], alpha=0.08)

point, = ax_side.plot(r2_sweep[0] / 1000, vout_values[0], "o",
                      color=theme.ACCENT, markersize=10, zorder=10,
                      markeredgecolor=theme.FG, markeredgewidth=1)

vline, = ax_side.plot([r2_sweep[0] / 1000, r2_sweep[0] / 1000],
                      [0, vout_values[0]], color=theme.ACCENT,
                      linewidth=1, linestyle=":", alpha=0.5)

hline, = ax_side.plot([0, r2_sweep[0] / 1000],
                      [vout_values[0], vout_values[0]], color=theme.ACCENT,
                      linewidth=1, linestyle=":", alpha=0.5)

ax_side.set_xlabel("R$_2$ (kΩ)")
ax_side.set_ylabel("V$_{out}$ (V)")
ax_side.set_title("V$_{out}$ varies with R$_2$", fontsize=12)
ax_side.grid(True, alpha=0.4)
ax_side.set_xlim(0, R2_MAX / 1000)
ax_side.set_ylim(0, VIN * 1.05)

# ======================= HEADER / FOOTER =======================
theme.header(fig,
    "Voltage Divider",
    "R$_2$ sweeps 0 → 10 kΩ — V$_{out}$ = V$_{in}$ · R$_2$/(R$_1$ + R$_2$)")
theme.footer(fig,
    f"V$_{{in}}$={VIN}V  R$_1$={R1}Ω  R$_2$=0–{R2_MAX}Ω  ideal divider, no load",
    handle="code.arts")

# ======================= ANIMATION =======================
prev_vout = [vout_values[0]]

def update(frame):
    v_curr = vout_values[frame]
    r2_curr = r2_sweep[frame]
    vr1 = VIN - v_curr

    top_fill.set_y(v_curr)
    top_fill.set_height(vr1)
    bot_fill.set_height(v_curr)
    rail_hl.set_ydata([0, v_curr])
    marker.set_ydata([v_curr])
    prev_tick.set_ydata([prev_vout[0], prev_vout[0]])
    vout_text.set_y(v_curr)
    vout_text.set_text(f"V$_{{out}}$ = {v_curr:.2f} V")
    anno_line.set_ydata([v_curr, v_curr])
    r1_comp.set_y((VIN + v_curr) / 2)
    r2_comp.set_y(v_curr / 2)
    r2_comp.set_text(f"R$_2$ = {r2_curr/1000:.2f} kΩ")
    vr1_text.set_y((VIN + v_curr) / 2)
    vr1_text.set_text(f"{vr1:.1f}V")
    vr2_text.set_y(v_curr / 2)
    vr2_text.set_text(f"{v_curr:.1f}V")

    point.set_data([r2_curr / 1000], [v_curr])
    vline.set_data([r2_curr / 1000, r2_curr / 1000], [0, v_curr])
    hline.set_data([0, r2_curr / 1000], [v_curr, v_curr])

    prev_vout[0] = v_curr

anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/voltage_divider.gif", fps=20)
plt.close(fig)
