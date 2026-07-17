import numpy as np
from builder import FigureBuilder
from physics.phase_2.filter import magnitude_db, step_response, phase_deg, corner_freq_rc

R = 1_000
C = 1e-6
FC = corner_freq_rc(R, C)
TAU = R * C

f_full = np.logspace(0, 5, 300)
t_step = np.linspace(0, 5 * TAU, 300)

mag = magnitude_db(f_full, FC)
step = step_response(t_step, TAU)

fig = FigureBuilder(
    title="What \u22123 dB actually costs you",
    subtitle="Magnitude alone hides the time-domain penalty \u2014 as f passes fc, amplitude drops and phase lag grows",
    footer="R=1k\u03a9  C=1\u03bcF  fc=159Hz  \u03c4=1.0ms  idealized first-order LP, no parasitics",
)

fig.ax_hero.semilogx(f_full, mag, color=fig.accent, linewidth=2.5)
fig.ax_hero.fill_between(f_full, mag, alpha=0.08, color=fig.accent)

fig.add_threshold(fig.ax_hero, FC, axis="x", label="fc")
fig.add_callout(fig.ax_hero, FC, -3, f"\u22123 dB @ fc = {FC:.0f} Hz")

fig.ax_hero.set_xlim(10, 1e5)
fig.ax_hero.set_ylim(-42, 3)
fig.ax_hero.set_xlabel("Frequency (Hz)")
fig.ax_hero.set_ylabel("|H(j\u03c9)| (dB)")
fig.ax_hero.set_title("Bode magnitude: \u221220 dB/decade past \u03c9\u2080", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

fig.ax_side.plot(t_step * 1000, step, color=fig.series[1], linewidth=2.5, zorder=3)
fig.ax_side.fill_between(t_step * 1000, step, color=fig.series[1], alpha=0.08)
fig.add_threshold(fig.ax_side, TAU * 1000, axis="x", label="\u03c4")
fig.add_threshold(fig.ax_side, 0.632, axis="y", label="63.2%")
fig.ax_side.set_xlim(0, 5 * TAU * 1000)
fig.ax_side.set_ylim(0, 1.1)
fig.ax_side.set_xlabel("Time (ms)")
fig.ax_side.set_ylabel("V$_{out}$ / V$_{in}$")
fig.ax_side.set_title("Step response at fc: \u03c4 = 1.0 ms", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

fig.save("filter_response.png")

n_frames = 100
f_sweep = np.logspace(np.log10(10), np.log10(1e5), n_frames)

cycles = np.linspace(0, 2, 200)
vin_all = np.sin(2 * np.pi * cycles)
vout_all = np.array([
    (10 ** (magnitude_db(f, FC) / 20)) * np.sin(2 * np.pi * cycles + np.radians(phase_deg(f, FC)))
    for f in f_sweep
])

for artist in fig.ax_side.get_lines() + fig.ax_side.collections:
    artist.set_visible(False)
fig.ax_side.set_xlim(0, 2)
fig.ax_side.set_ylim(-1.8, 1.8)
fig.ax_side.set_xlabel("Cycles")
fig.ax_side.set_ylabel("Amplitude")
fig.ax_side.set_title("Sinusoidal response at f = {:.0f} Hz", fontsize=11)

vin_line, = fig.ax_side.plot(cycles, vin_all, color=fig.muted, linewidth=1.5,
                              linestyle="--", alpha=0.6)
vout_line, = fig.ax_side.plot(cycles, vout_all[0], color=fig.series[1], linewidth=2.5)
side_label = fig.ax_side.text(0.5, 1.6, "", color=fig.fg, fontsize=10,
                               fontfamily=fig.font_mono, ha="center")

hero_dot, = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                              markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
hero_label = fig.ax_hero.text(0.96, 0.15, "", color=fig.fg, fontsize=9,
                               fontfamily=fig.font_mono, ha="right", va="top",
                               transform=fig.ax_hero.transAxes)


def update(frame):
    f = f_sweep[frame]
    g = magnitude_db(f, FC)
    phi = phase_deg(f, FC)

    hero_dot.set_data([f], [g])
    hero_label.set_text(f"f = {f:.0f} Hz  |  |H| = {g:.1f} dB  |  \u03c6 = {phi:.1f}\u00b0")

    vout_line.set_data(cycles, vout_all[frame])
    side_label.set_text(f"f = {f:.0f} Hz  |  |H| = {10**(g/20):.3f}  |  \u03c6 = {phi:.1f}\u00b0")


fig.animate(n_frames, update, "filter_response.gif", fps=20)
