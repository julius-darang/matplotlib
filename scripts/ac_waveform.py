import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

import theme
from animate import make_animation, save_gif
from physics.ac_waveform import sine_wave, deg_to_rad

theme.apply()

# --- circuit parameters ---------------------------------------------------
A = 1.0           # amplitude (V)
f = 1.0           # frequency (Hz)
phi_deg = 60.0    # phase shift (degrees)
phi = deg_to_rad(phi_deg)

# --- time axis ------------------------------------------------------------
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

# --- figure ---------------------------------------------------------------
fig = plt.figure(figsize=(11, 6.2))
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.5, 1],
              left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3)

ax_hero = fig.add_subplot(gs[0, 0])
ax_side = fig.add_subplot(gs[0, 1])

# ======================= HERO — Time Domain ===============================
ax_hero.plot(t_full, ref_full, color=theme.MUTED, linewidth=1.8, zorder=2, alpha=0.7)
ax_hero.plot(t_full, shift_full, color=theme.ACCENT, linewidth=2.5, zorder=3)

# Phase shift bracket between corresponding rising zero crossings
t_shift_zero = 1.0 - dt   # shifted rising zero at t = 5/6
t_ref_zero = 1.0           # reference rising zero at t = 1.0
ax_hero.axvline(t_shift_zero, color=theme.ACCENT, linestyle=":", linewidth=1, alpha=0.5)
ax_hero.axvline(t_ref_zero, color=theme.MUTED, linestyle=":", linewidth=1, alpha=0.5)
ax_hero.annotate("", xy=(t_shift_zero, -A * 1.15), xytext=(t_ref_zero, -A * 1.15),
                arrowprops=dict(arrowstyle="<->", color=theme.MUTED, lw=1.5))
ax_hero.text((t_shift_zero + t_ref_zero) / 2, -A * 1.25, f"φ = {phi_deg:.0f}°",
            color=theme.ACCENT, fontsize=11, fontfamily=theme.FONT_MONO,
            ha="center", va="top")

# Legend
legend_elements = [
    Line2D([0], [0], color=theme.MUTED, linewidth=1.8, alpha=0.7,
           label="v(t) = A · sin(ωt)"),
    Line2D([0], [0], color=theme.ACCENT, linewidth=2.5,
           label=f"v(t) = A · sin(ωt + {phi_deg:.0f}°)"),
]
ax_hero.legend(handles=legend_elements, loc="upper left", fontsize=8,
              labelcolor=theme.FG, framealpha=0.2)

ax_hero.set_xlim(0, t_max)
ax_hero.set_ylim(-A * 1.4, A * 1.35)
ax_hero.set_xlabel("Time (s)")
ax_hero.set_ylabel("v(t) (V)")
ax_hero.set_title("AC Waveform — Phase Shift", fontsize=11)
ax_hero.grid(True, alpha=0.3)

# Animated artists
hero_dot_ref,   = ax_hero.plot([], [], "o", color=theme.MUTED, markersize=8,
                               markeredgecolor=theme.FG, markeredgewidth=1.2,
                               zorder=10, alpha=0.7)
hero_dot_shift, = ax_hero.plot([], [], "o", color=theme.ACCENT, markersize=10,
                               markeredgecolor=theme.FG, markeredgewidth=1.5,
                               zorder=10)
hero_vline, = ax_hero.plot([], [], color=theme.FG, linewidth=1,
                           linestyle="--", alpha=0.25)
hero_time = ax_hero.text(0.95, 0.95, "", color=theme.FG, fontsize=10,
                         fontfamily=theme.FONT_MONO, ha="right", va="top",
                         transform=ax_hero.transAxes)

# ======================= SIDE — Phasor Diagram ============================
th_circ = np.linspace(0, 2 * np.pi, 200)
ax_side.plot(np.cos(th_circ), np.sin(th_circ), color=theme.GRID,
             linewidth=1, alpha=0.5)
ax_side.axhline(0, color=theme.GRID, linewidth=0.5, alpha=0.3)
ax_side.axvline(0, color=theme.GRID, linewidth=0.5, alpha=0.3)

# Phasors (updated during animation)
ref_phasor,   = ax_side.plot([], [], color=theme.MUTED, linewidth=2,
                             alpha=0.7, zorder=5)
shift_phasor, = ax_side.plot([], [], color=theme.ACCENT, linewidth=2.5,
                             zorder=5)
ref_tip,  = ax_side.plot([], [], "o", color=theme.MUTED, markersize=8,
                         alpha=0.7, zorder=6)
shift_tip, = ax_side.plot([], [], "o", color=theme.ACCENT, markersize=8,
                          zorder=6)

# Static φ label just above ωt label
ax_side.text(0.95, 0.14, f"φ = {phi_deg:.0f}°",
            color=theme.ACCENT, fontsize=10, fontfamily=theme.FONT_MONO,
            ha="right", va="bottom", transform=ax_side.transAxes,
            fontweight="bold")

ax_side.set_xlim(-1.3, 1.3)
ax_side.set_ylim(-1.3, 1.3)
ax_side.set_aspect("equal")
ax_side.set_xlabel("Real")
ax_side.set_ylabel("Imag")
ax_side.set_title("Phasor Diagram", fontsize=11)
ax_side.grid(True, alpha=0.3)

side_angle = ax_side.text(0.95, 0.05, "", color=theme.FG, fontsize=9,
                          fontfamily=theme.FONT_MONO, ha="right", va="bottom",
                          transform=ax_side.transAxes)

# ======================= HEADER / FOOTER ==================================
theme.header(fig,
    "AC Waveform — Phase Shift",
    f"A {A:.0f}V sine wave at {f:.0f} Hz with a {phi_deg:.0f}° phase shift")
theme.footer(fig,
    f"A={A:.0f}V  f={f:.0f}Hz  φ={phi_deg:.0f}°  "
    f"Δt = φ/(2πf) = {dt:.3f}s",
    handle="code.arts")

# ======================= ANIMATION ========================================
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
    side_angle.set_text(f"ωt = {np.rad2deg(th):.0f}°")

anim = make_animation(fig, update, n_frames, fps=20)
save_gif(anim, "outputs/ac_waveform.gif", fps=20)
plt.close(fig)
