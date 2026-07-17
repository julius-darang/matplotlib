import numpy as np
from builder import FigureBuilder
from physics.resonant_frequency import f0, f0_curve

fig = FigureBuilder(
    title="Resonant Frequency",
    subtitle="f\u2080 = 1 / (2\u03c0\u221aLC) \u2014 sweeping C shows the inverse-square-root sensitivity",
    footer="L = 10.0 mH  C = 1.00 \u03bcF  f\u2080 = 1592 Hz  ideal LC, no resistance",
)

L = 10e-3
C_BASE = 1e-6
F0_BASE = f0(L, C_BASE)

C_MIN = C_BASE / 3.0
C_MAX = C_BASE * 3.0

n_frames = 100
c_sweep = np.geomspace(C_MIN, C_MAX, n_frames)
f0_sweep = f0_curve(c_sweep, L)

c_full = np.geomspace(C_MIN, C_MAX, 300)
f0_full = f0_curve(c_full, L)

F_MIN, F_MAX = 100, 10000

fig.ax_hero.spines[:].set_visible(False)
fig.ax_hero.set_xticks([])
fig.ax_hero.set_yticks([])
fig.ax_hero.set_xlim(F_MIN, F_MAX)
fig.ax_hero.set_ylim(-0.5, 5)
fig.ax_hero.set_xscale("log")
fig.ax_hero.set_title("Resonant frequency f\u2080 = 1 / (2\u03c0\u221aLC)", fontsize=11)

fig.ax_hero.plot([F_MIN, F_MAX], [0, 0], color=fig.grid, linewidth=2, zorder=1)

for decade_exp in range(int(np.log10(F_MIN)), int(np.log10(F_MAX)) + 1):
    freq = 10 ** decade_exp
    if F_MIN <= freq <= F_MAX:
        fig.ax_hero.plot([freq, freq], [-0.3, 0.3], color=fig.muted, linewidth=1.2)

fig.ax_hero.text(F_MAX * 1.1, 0, "f (Hz)", color=fig.muted, fontsize=9,
                 fontfamily=fig.font_mono, va="center")

hero_f0_line, = fig.ax_hero.plot([F0_BASE, F0_BASE], [0, 3.5], color=fig.accent,
                                  linewidth=2.5, zorder=4)
hero_dot, = fig.ax_hero.plot([F0_BASE], [3.5], "o", color=fig.accent, markersize=14,
                              markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=8)

readout_text = fig.ax_hero.text(0.07, 0.78, "", color=fig.fg, fontsize=8,
                                fontfamily=fig.font_mono, va="top",
                                transform=fig.ax_hero.transAxes, zorder=7)

fig.ax_side.plot(c_full * 1e6, f0_full, color=fig.series[1], linewidth=2.5, zorder=3)
fig.ax_side.fill_between(c_full * 1e6, f0_full, color=fig.series[1], alpha=0.08)

fig.ax_side.set_xscale("log")
fig.ax_side.set_yscale("log")
fig.ax_side.set_xlabel("Capacitance (\u03bcF)")
fig.ax_side.set_ylabel("f\u2080 (Hz)")
fig.ax_side.set_title("f\u2080 \u221d 1 / \u221aC \u2014 inverse square root", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)
fig.ax_side.set_xlim(C_MIN * 1e6, C_MAX * 1e6)
fig.ax_side.set_ylim(f0_full[-1] * 0.8, f0_full[0] * 1.2)

side_dot, = fig.ax_side.plot([], [], "o", color=fig.accent, markersize=10,
                              markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
side_vline, = fig.ax_side.plot([], [], color=fig.accent, linewidth=1,
                                linestyle="--", alpha=0.4)
side_label = fig.ax_side.text(0.05, 0.95, "", color=fig.fg, fontsize=10,
                              fontfamily=fig.font_mono, ha="left", va="top",
                              transform=fig.ax_side.transAxes)


def update(frame):
    c_curr = c_sweep[frame]
    f0_curr = f0_sweep[frame]

    hero_f0_line.set_xdata([f0_curr, f0_curr])
    hero_dot.set_xdata([f0_curr])

    readout_text.set_text(
        f"   L = {L*1e3:.1f} mH\n"
        f"   C = {c_curr*1e6:.2f} \u03bcF\n"
        f"   f\u2080 = {f0_curr:.0f} Hz"
    )

    side_dot.set_data([c_curr * 1e6], [f0_curr])
    side_vline.set_data([c_curr * 1e6, c_curr * 1e6],
                        [fig.ax_side.get_ylim()[0], f0_curr])
    side_label.set_text(f"C = {c_curr*1e6:.2f} \u03bcF\nf\u2080 = {f0_curr:.0f} Hz")


fig.animate(n_frames, update, "resonant_frequency.gif", fps=20)
