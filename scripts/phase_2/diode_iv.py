import numpy as np
from builder import FigureBuilder
from physics.phase_2.diode_iv import v_thermal, isat, diode_current, turn_on_voltage

fig = FigureBuilder(
    title="Why diode turn-on voltage drops as temperature rises",
    subtitle="Is(T) doubles every 10\u00b0C, overwhelming V_T = kT/q's slight rise and shifting the whole curve left",
    footer="n=1.5  Is\u2080=1pA @25\u00b0C  Is(T)\u2248Is\u2080\u00b72^((T\u221225)/10) (rule-of-thumb approximation)  V_on @ I=100\u00b5A",
)

V_MIN, V_MAX = -0.2, 1.0
V_FULL = np.linspace(V_MIN, V_MAX, 1000)
T_MIN, T_MAX = 0, 100
N_FRAMES = 100
T_SWEEP = np.linspace(T_MIN, T_MAX, N_FRAMES)

I_INIT = diode_current(V_FULL, 0.0)

H_Y_MIN, H_Y_MAX = -1e-3, 10e-3

fig.ax_hero.axvspan(V_MIN, 0, color=fig.muted, alpha=0.07, zorder=0)
fig.ax_hero.axvspan(0.50, 0.85, color=fig.accent, alpha=0.06, zorder=0)

hero_curve, = fig.ax_hero.plot(V_FULL, I_INIT, color=fig.accent, linewidth=2.5, zorder=3)
hero_thresh, = fig.ax_hero.plot([], [], color=fig.accent, linestyle="--", linewidth=1.5, alpha=0.7, zorder=5)
hero_callout = fig.ax_hero.text(
    0.03, 0.96, "", color=fig.fg, fontsize=9,
    fontfamily=fig.font_mono, ha="left", va="top",
    transform=fig.ax_hero.transAxes,
    bbox=dict(boxstyle="round,pad=0.3", facecolor=fig.bg,
              edgecolor=fig.muted, linewidth=0.5),
)

fig.ax_hero.set_xlim(V_MIN, V_MAX)
fig.ax_hero.set_ylim(H_Y_MIN, H_Y_MAX)
fig.ax_hero.set_xlabel("Forward voltage (V)")
fig.ax_hero.set_ylabel("Current (A)")
fig.ax_hero.set_title("I\u2013V characteristic (linear)", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

S_Y_MIN, S_Y_MAX = 1e-13, 1e-1

side_curve, = fig.ax_side.plot(V_FULL, np.maximum(I_INIT, 1e-15),
                                color=fig.accent, linewidth=2.5, zorder=3)
fig.ax_side.set_yscale("log")

side_thresh, = fig.ax_side.plot([], [], color=fig.accent, linestyle="--",
                                 linewidth=1.5, alpha=0.7, zorder=5)
side_callout = fig.ax_side.text(
    0.03, 0.96, "", color=fig.fg, fontsize=9,
    fontfamily=fig.font_mono, ha="left", va="top",
    transform=fig.ax_side.transAxes,
    bbox=dict(boxstyle="round,pad=0.3", facecolor=fig.bg,
              edgecolor=fig.muted, linewidth=0.5),
)

fig.ax_side.set_xlim(V_MIN, V_MAX)
fig.ax_side.set_ylim(S_Y_MIN, S_Y_MAX)
fig.ax_side.set_xlabel("Forward voltage (V)")
fig.ax_side.set_ylabel("Current (A)")
fig.ax_side.set_title("I\u2013V characteristic (log)", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)


def update(frame):
    t = T_SWEEP[frame]
    i = diode_current(V_FULL, t)
    v_on = turn_on_voltage(t)

    hero_curve.set_data(V_FULL, i)
    hero_thresh.set_data([v_on, v_on], [H_Y_MIN, H_Y_MAX])
    hero_callout.set_text(f"T = {t:.0f}\u00b0C\nV_on = {v_on:.3f}V")

    side_curve.set_data(V_FULL, np.maximum(i, 1e-15))
    side_thresh.set_data([v_on, v_on], [S_Y_MIN, S_Y_MAX])
    side_callout.set_text(f"T = {t:.0f}\u00b0C\nV_on = {v_on:.3f}V")


fig.animate(N_FRAMES, update, "diode_iv.gif", fps=20)
