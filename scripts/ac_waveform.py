import numpy as np
from matplotlib.lines import Line2D
from builder import FigureBuilder
from physics.ac_waveform import sine_wave, deg_to_rad

fig = FigureBuilder(
    title="AC Waveform \u2014 Phase Shift",
    subtitle="A 1V sine wave at 1 Hz with a 60\u00b0 phase shift",
    footer="A=1V  f=1Hz  \u03c6=60\u00b0  \u0394t = \u03c6/(2\u03c0f) = 0.167s",
)

A = 1.0
f = 1.0
phi_deg = 60.0
phi = deg_to_rad(phi_deg)

T = 1.0 / f
t_max = 2 * T
t_full = np.linspace(0, t_max, 400)

n_frames = 100
t_sweep = np.linspace(0, t_max, n_frames)

ref_full = sine_wave(t_full, A, f, 0)
shift_full = sine_wave(t_full, A, f, phi)
ref_anim = sine_wave(t_sweep, A, f, 0)
shift_anim = sine_wave(t_sweep, A, f, phi)

theta = 2 * np.pi * f * t_sweep
dt = phi / (2 * np.pi * f)

fig.ax_hero.plot(t_full, ref_full, color=fig.muted, linewidth=1.8, zorder=2, alpha=0.7)
fig.ax_hero.plot(t_full, shift_full, color=fig.accent, linewidth=2.5, zorder=3)

t_shift_zero = 1.0 - dt
t_ref_zero = 1.0
fig.ax_hero.axvline(t_shift_zero, color=fig.accent, linestyle=":", linewidth=1, alpha=0.5)
fig.ax_hero.axvline(t_ref_zero, color=fig.muted, linestyle=":", linewidth=1, alpha=0.5)
fig.ax_hero.annotate("", xy=(t_shift_zero, -A * 1.15), xytext=(t_ref_zero, -A * 1.15),
                     arrowprops=dict(arrowstyle="<->", color=fig.muted, lw=1.5))
fig.ax_hero.text((t_shift_zero + t_ref_zero) / 2, -A * 1.25, f"\u03c6 = {phi_deg:.0f}\u00b0",
                 color=fig.accent, fontsize=11, fontfamily=fig.font_mono,
                 ha="center", va="top")

legend_elements = [
    Line2D([0], [0], color=fig.muted, linewidth=1.8, alpha=0.7,
           label="v(t) = A \u00b7 sin(\u03c9t)"),
    Line2D([0], [0], color=fig.accent, linewidth=2.5,
           label=f"v(t) = A \u00b7 sin(\u03c9t + {phi_deg:.0f}\u00b0)"),
]
fig.ax_hero.legend(handles=legend_elements, loc="upper left", fontsize=8,
                   labelcolor=fig.fg, framealpha=0.2)

fig.ax_hero.set_xlim(0, t_max)
fig.ax_hero.set_ylim(-A * 1.4, A * 1.35)
fig.ax_hero.set_xlabel("Time (s)")
fig.ax_hero.set_ylabel("v(t) (V)")
fig.ax_hero.set_title("AC Waveform \u2014 Phase Shift", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

hero_dot_ref,   = fig.ax_hero.plot([], [], "o", color=fig.muted, markersize=8,
                                   markeredgecolor=fig.fg, markeredgewidth=1.2,
                                   zorder=10, alpha=0.7)
hero_dot_shift, = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                                   markeredgecolor=fig.fg, markeredgewidth=1.5,
                                   zorder=10)
hero_vline, = fig.ax_hero.plot([], [], color=fig.fg, linewidth=1,
                               linestyle="--", alpha=0.25)
hero_time = fig.ax_hero.text(0.95, 0.95, "", color=fig.fg, fontsize=10,
                             fontfamily=fig.font_mono, ha="right", va="top",
                             transform=fig.ax_hero.transAxes)

th_circ = np.linspace(0, 2 * np.pi, 200)
fig.ax_side.plot(np.cos(th_circ), np.sin(th_circ), color=fig.grid,
                 linewidth=1, alpha=0.5)
fig.ax_side.axhline(0, color=fig.grid, linewidth=0.5, alpha=0.3)
fig.ax_side.axvline(0, color=fig.grid, linewidth=0.5, alpha=0.3)

ref_phasor,   = fig.ax_side.plot([], [], color=fig.muted, linewidth=2,
                                 alpha=0.7, zorder=5)
shift_phasor, = fig.ax_side.plot([], [], color=fig.accent, linewidth=2.5,
                                 zorder=5)
ref_tip,  = fig.ax_side.plot([], [], "o", color=fig.muted, markersize=8,
                             alpha=0.7, zorder=6)
shift_tip, = fig.ax_side.plot([], [], "o", color=fig.accent, markersize=8,
                              zorder=6)

fig.ax_side.text(0.95, 0.14, f"\u03c6 = {phi_deg:.0f}\u00b0",
                 color=fig.accent, fontsize=10, fontfamily=fig.font_mono,
                 ha="right", va="bottom", transform=fig.ax_side.transAxes,
                 fontweight="bold")

fig.ax_side.set_xlim(-1.3, 1.3)
fig.ax_side.set_ylim(-1.3, 1.3)
fig.ax_side.set_aspect("equal")
fig.ax_side.set_xlabel("Real")
fig.ax_side.set_ylabel("Imag")
fig.ax_side.set_title("Phasor Diagram", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

side_angle = fig.ax_side.text(0.95, 0.05, "", color=fig.fg, fontsize=9,
                              fontfamily=fig.font_mono, ha="right", va="bottom",
                              transform=fig.ax_side.transAxes)


def update(frame):
    t = t_sweep[frame]
    vr = ref_anim[frame]
    vs = shift_anim[frame]
    th = theta[frame]

    hero_dot_ref.set_data([t], [vr])
    hero_dot_shift.set_data([t], [vs])
    hero_vline.set_data([t, t], [-A * 1.4, A * 1.35])
    hero_time.set_text(f"t = {t:.2f}s")

    rx, ry = np.cos(th), np.sin(th)
    sx, sy = np.cos(th + phi), np.sin(th + phi)
    ref_phasor.set_data([0, rx], [0, ry])
    shift_phasor.set_data([0, sx], [0, sy])
    ref_tip.set_data([rx], [ry])
    shift_tip.set_data([sx], [sy])
    side_angle.set_text(f"\u03c9t = {np.rad2deg(th):.0f}\u00b0")


fig.animate(n_frames, update, "ac_waveform.gif", fps=20)
