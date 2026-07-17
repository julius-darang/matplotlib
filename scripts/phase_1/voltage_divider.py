import numpy as np
import matplotlib.pyplot as plt
from builder import FigureBuilder
from physics.phase_1.voltage_divider import vout

fig = FigureBuilder(
    title="Voltage Divider",
    subtitle="R\u2082 sweeps 0 \u2192 10 k\u03a9 \u2014 V\u208ent = V\u2081\u00b7 R\u2082/(R\u2081 + R\u2082)",
    footer="V_in=12V  R\u2081=1000\u03a9  R\u2082=0\u201310000\u03a9  ideal divider, no load",
)

VIN = 12.0
R1 = 1_000
R2_MAX = 10_000

n_ramp = 80
r2_forward = np.linspace(0, R2_MAX, n_ramp)
r2_backward = np.linspace(R2_MAX, 0, n_ramp)
r2_sweep = np.concatenate([r2_forward, r2_backward])
n_frames = len(r2_sweep)

vout_values = vout(VIN, R1, r2_sweep)

fig.ax_hero.spines[:].set_visible(False)
fig.ax_hero.set_xticks([])
fig.ax_hero.set_yticks([])
fig.ax_hero.set_xlim(-1.2, 3.5)
fig.ax_hero.set_ylim(-1.0, VIN + 1.5)
fig.ax_hero.set_title("V$_{total}$ split by R$_1$ and R$_2$", fontsize=12)

VOLTS = [0.0, 3.0, 6.0, 9.0, 12.0]
VSTR = ["0", "3V", "6V", "9V", "V$_{in}$"]
for v, s in zip(VOLTS, VSTR):
    fig.ax_hero.plot([-0.06, 0], [v, v], color=fig.muted, linewidth=0.8)
    fig.ax_hero.text(-0.22, v, s, color=fig.muted, fontsize=9,
                     fontfamily=fig.font_mono, va="center", ha="right")

fig.ax_hero.plot([0, 0], [0, VIN], color=fig.grid, linewidth=3, zorder=1)

top_fill = plt.Rectangle((-0.06, vout_values[0]), 0.12, VIN - vout_values[0],
                          color=fig.muted, alpha=0.06, zorder=2)
fig.ax_hero.add_patch(top_fill)

bot_fill = plt.Rectangle((-0.06, 0), 0.12, vout_values[0],
                          color=fig.accent, alpha=0.12, zorder=2)
fig.ax_hero.add_patch(bot_fill)

rail_hl, = fig.ax_hero.plot([0, 0], [0, vout_values[0]], color=fig.accent,
                            linewidth=3, solid_capstyle="round", zorder=3)

marker, = fig.ax_hero.plot([0], [vout_values[0]], "o", color=fig.accent,
                           markersize=14, markeredgecolor=fig.fg,
                           markeredgewidth=1.5, zorder=10)

prev_tick, = fig.ax_hero.plot([-0.08, 0.08], [vout_values[0], vout_values[0]],
                              color=fig.muted, linewidth=1.5, alpha=0.35, zorder=5)

vout_text = fig.ax_hero.text(0.3, vout_values[0], f"V$_{{out}}$ = {vout_values[0]:.2f} V",
                             color=fig.fg, fontsize=11, fontfamily=fig.font_mono,
                             va="center")

anno_line, = fig.ax_hero.plot([0.06, 0.25], [vout_values[0], vout_values[0]],
                              color=fig.muted, linewidth=0.8, alpha=0.6, zorder=4)

r1_comp = fig.ax_hero.text(0.3, (VIN + vout_values[0]) / 2,
                            f"R$_1$ = {R1/1000:.1f} k\u03a9",
                            color=fig.muted, fontsize=10, fontfamily=fig.font_mono,
                            va="center")

r2_comp = fig.ax_hero.text(0.3, vout_values[0] / 2,
                            f"R$_2$ = {r2_sweep[0]/1000:.2f} k\u03a9",
                            color=fig.accent, fontsize=10, fontfamily=fig.font_mono,
                            va="center")

vr1_text = fig.ax_hero.text(-0.15, (VIN + vout_values[0]) / 2,
                             f"{VIN - vout_values[0]:.1f}V",
                             color=fig.muted, fontsize=8, fontfamily=fig.font_mono,
                             va="center", ha="right")

vr2_text = fig.ax_hero.text(-0.15, vout_values[0] / 2,
                             f"{vout_values[0]:.1f}V",
                             color=fig.accent, fontsize=8, fontfamily=fig.font_mono,
                             va="center", ha="right")

fig.ax_hero.plot([-0.04, 0.04], [VIN, VIN], color=fig.grid, linewidth=1.5)

fig.ax_hero.text(0, VIN + 0.5, "V$_{total}$", color=fig.muted, fontsize=10,
                 fontfamily=fig.font_sans, ha="center", va="bottom")

r2_full = np.linspace(0, R2_MAX, 200)
vout_full = vout(VIN, R1, r2_full)

fig.ax_side.plot(r2_full / 1000, vout_full, color=fig.series[1], linewidth=2.5, zorder=1)
fig.ax_side.fill_between(r2_full / 1000, vout_full, color=fig.series[1], alpha=0.08)

point, = fig.ax_side.plot(r2_sweep[0] / 1000, vout_values[0], "o",
                          color=fig.accent, markersize=10, zorder=10,
                          markeredgecolor=fig.fg, markeredgewidth=1)

vline, = fig.ax_side.plot([r2_sweep[0] / 1000, r2_sweep[0] / 1000],
                          [0, vout_values[0]], color=fig.accent,
                          linewidth=1, linestyle=":", alpha=0.5)

hline, = fig.ax_side.plot([0, r2_sweep[0] / 1000],
                          [vout_values[0], vout_values[0]], color=fig.accent,
                          linewidth=1, linestyle=":", alpha=0.5)

fig.ax_side.set_xlabel("R$_2$ (k\u03a9)")
fig.ax_side.set_ylabel("V$_{out}$ (V)")
fig.ax_side.set_title("V$_{out}$ varies with R$_2$", fontsize=12)
fig.ax_side.grid(True, alpha=0.4)
fig.ax_side.set_xlim(0, R2_MAX / 1000)
fig.ax_side.set_ylim(0, VIN * 1.05)

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
    r2_comp.set_text(f"R$_2$ = {r2_curr/1000:.2f} k\u03a9")
    vr1_text.set_y((VIN + v_curr) / 2)
    vr1_text.set_text(f"{vr1:.1f}V")
    vr2_text.set_y(v_curr / 2)
    vr2_text.set_text(f"{v_curr:.1f}V")

    point.set_data([r2_curr / 1000], [v_curr])
    vline.set_data([r2_curr / 1000, r2_curr / 1000], [0, v_curr])
    hline.set_data([0, r2_curr / 1000], [v_curr, v_curr])

    prev_vout[0] = v_curr


fig.animate(n_frames, update, "voltage_divider.gif", fps=20)
