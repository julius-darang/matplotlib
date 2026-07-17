import numpy as np
from builder import FigureBuilder
from physics.phase_1.inductor import i_buildup, i_decay, time_constant

fig = FigureBuilder(
    title="RL Time Constant",
    subtitle="Current buildup and decay \u2014 the same \u03c4 = L/R governs both directions",
    footer="V_S=5.0V  R=1\u03a9  L=2H  \u03c4 = L/R = 2.00s",
)

V_SOURCE = 5.0
R = 1
L = 2
TAU = time_constant(R, L)

t_max = 5 * TAU
t_full = np.linspace(0, t_max, 300)
n_frames = 100
t_sweep = np.linspace(0, t_max, n_frames)

i_max = V_SOURCE / R

buildup_full = i_buildup(t_full, V_SOURCE, R, TAU)
decay_full   = i_decay(t_full, i_max, TAU)
buildup_anim = i_buildup(t_sweep, V_SOURCE, R, TAU)
decay_anim   = i_decay(t_sweep, i_max, TAU)

fig.ax_hero.plot(t_full, buildup_full, color=fig.accent, linewidth=2.5, zorder=3)
fig.ax_hero.fill_between(t_full, buildup_full, color=fig.accent, alpha=0.08)

fig.ax_hero.axvline(TAU, color=fig.muted, linestyle="--", linewidth=1.2, alpha=0.7)
fig.ax_hero.text(TAU, i_max * -0.08, "\u03c4", color=fig.muted,
                 fontsize=11, fontfamily=fig.font_mono, ha="center", va="top")

i_63 = i_max * (1 - np.exp(-1))
fig.ax_hero.axhline(i_63, color=fig.muted, linestyle=":", linewidth=1, alpha=0.5)
fig.ax_hero.text(t_max * 0.02, i_63, "  63 %", color=fig.muted, fontsize=9,
                 fontfamily=fig.font_mono, va="bottom")

fig.ax_hero.set_xlim(0, t_max)
fig.ax_hero.set_ylim(0, i_max * 1.15)
fig.ax_hero.set_xlabel("Time (s)")
fig.ax_hero.set_ylabel("I$_{L}$ (A)")
fig.ax_hero.set_title("Buildup: I(t) = (V$_{S}$/R)(1 \u2212 e$^{-t/\u03c4}$)", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

hero_dot,   = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                                markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
hero_vline, = fig.ax_hero.plot([], [], color=fig.accent, linewidth=1,
                                linestyle="--", alpha=0.4)
hero_label  = fig.ax_hero.text(0.95, 0.95, "", color=fig.fg, fontsize=10,
                                fontfamily=fig.font_mono, ha="right", va="top",
                                transform=fig.ax_hero.transAxes)

fig.ax_side.plot(t_full, decay_full, color=fig.series[1], linewidth=2.5, zorder=3)
fig.ax_side.fill_between(t_full, decay_full, color=fig.series[1], alpha=0.08)

fig.ax_side.axvline(TAU, color=fig.muted, linestyle="--", linewidth=1.2, alpha=0.7)
fig.ax_side.text(TAU, i_max * -0.08, "\u03c4", color=fig.muted,
                 fontsize=11, fontfamily=fig.font_mono, ha="center", va="top")

i_37 = i_max * np.exp(-1)
fig.ax_side.axhline(i_37, color=fig.muted, linestyle=":", linewidth=1, alpha=0.5)
fig.ax_side.text(t_max * 0.02, i_37, "  37 %", color=fig.muted, fontsize=9,
                 fontfamily=fig.font_mono, va="bottom")

fig.ax_side.set_xlim(0, t_max)
fig.ax_side.set_ylim(0, i_max * 1.15)
fig.ax_side.set_xlabel("Time (s)")
fig.ax_side.set_ylabel("I$_{L}$ (A)")
fig.ax_side.set_title("Decay: I(t) = (V$_{S}$/R) e$^{-t/\u03c4}$", fontsize=11)
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
    ib = buildup_anim[frame]
    ide = decay_anim[frame]

    hero_dot.set_data([t], [ib])
    hero_vline.set_data([t, t], [0, ib])
    hero_label.set_text(f"I = {ib:.2f} A")

    side_dot.set_data([t], [ide])
    side_vline.set_data([t, t], [0, ide])
    side_label.set_text(f"I = {ide:.2f} A")


fig.animate(n_frames, update, "inductor_rl.gif", fps=20)
