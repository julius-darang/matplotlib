import numpy as np
from builder import FigureBuilder
from physics.capacitor import v_charge, v_discharge, time_constant

fig = FigureBuilder(
    title="RC Time Constant",
    subtitle="Charge and discharge \u2014 the same \u03c4 = RC governs both directions",
    footer="V_S=5.0V  R=1k\u03a9  C=2000\u03bcF  \u03c4 = RC = 2.00s",
)

V_SOURCE = 5.0
R = 1_000
C = 2e-3
TAU = time_constant(R, C)

t_max = 5 * TAU
t_full = np.linspace(0, t_max, 300)
n_frames = 100
t_sweep = np.linspace(0, t_max, n_frames)

charge_full = v_charge(t_full, V_SOURCE, TAU)
disc_full   = v_discharge(t_full, V_SOURCE, TAU)
charge_anim = v_charge(t_sweep, V_SOURCE, TAU)
disc_anim   = v_discharge(t_sweep, V_SOURCE, TAU)

fig.ax_hero.plot(t_full, charge_full, color=fig.accent, linewidth=2.5, zorder=3)
fig.ax_hero.fill_between(t_full, charge_full, color=fig.accent, alpha=0.08)

fig.ax_hero.axvline(TAU, color=fig.muted, linestyle="--", linewidth=1.2, alpha=0.7)
fig.ax_hero.text(TAU, V_SOURCE * -0.08, "\u03c4", color=fig.muted,
                 fontsize=11, fontfamily=fig.font_mono, ha="center", va="top")

v_63 = V_SOURCE * (1 - np.exp(-1))
fig.ax_hero.axhline(v_63, color=fig.muted, linestyle=":", linewidth=1, alpha=0.5)
fig.ax_hero.text(t_max * 0.02, v_63, "  63 %", color=fig.muted, fontsize=9,
                 fontfamily=fig.font_mono, va="bottom")

fig.ax_hero.set_xlim(0, t_max)
fig.ax_hero.set_ylim(0, V_SOURCE * 1.15)
fig.ax_hero.set_xlabel("Time (s)")
fig.ax_hero.set_ylabel("V$_{C}$ (V)")
fig.ax_hero.set_title("Charging: V(t) = V$_{S}$(1 \u2212 e$^{-t/\u03c4}$)", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

hero_dot,   = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                                markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
hero_vline, = fig.ax_hero.plot([], [], color=fig.accent, linewidth=1,
                                linestyle="--", alpha=0.4)
hero_label  = fig.ax_hero.text(0.95, 0.95, "", color=fig.fg, fontsize=10,
                                fontfamily=fig.font_mono, ha="right", va="top",
                                transform=fig.ax_hero.transAxes)

fig.ax_side.plot(t_full, disc_full, color=fig.series[1], linewidth=2.5, zorder=3)
fig.ax_side.fill_between(t_full, disc_full, color=fig.series[1], alpha=0.08)

fig.ax_side.axvline(TAU, color=fig.muted, linestyle="--", linewidth=1.2, alpha=0.7)
fig.ax_side.text(TAU, V_SOURCE * -0.08, "\u03c4", color=fig.muted,
                 fontsize=11, fontfamily=fig.font_mono, ha="center", va="top")

v_37 = V_SOURCE * np.exp(-1)
fig.ax_side.axhline(v_37, color=fig.muted, linestyle=":", linewidth=1, alpha=0.5)
fig.ax_side.text(t_max * 0.02, v_37, "  37 %", color=fig.muted, fontsize=9,
                 fontfamily=fig.font_mono, va="bottom")

fig.ax_side.set_xlim(0, t_max)
fig.ax_side.set_ylim(0, V_SOURCE * 1.15)
fig.ax_side.set_xlabel("Time (s)")
fig.ax_side.set_ylabel("V$_{C}$ (V)")
fig.ax_side.set_title("Discharging: V(t) = V$_{S}$ e$^{-t/\u03c4}$", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

side_dot,   = fig.ax_side.plot([], [], "o", color=fig.series[1], markersize=10,
                                markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
side_vline, = fig.ax_side.plot([], [], color=fig.series[1], linewidth=1,
                                linestyle="--", alpha=0.4)
side_label  = fig.ax_side.text(0.95, 0.95, "", color=fig.fg, fontsize=10,
                                fontfamily=fig.font_mono, ha="right", va="top",
                                transform=fig.ax_side.transAxes)


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


fig.animate(n_frames, update, "capacitor_rc.gif", fps=20)
