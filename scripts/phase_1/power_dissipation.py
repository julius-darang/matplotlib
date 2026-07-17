import numpy as np
from builder import FigureBuilder
from physics.phase_1.power_dissipation import power

fig = FigureBuilder(
    title="Power Dissipation",
    subtitle="The growing gap between I (linear) and P = I\u00b2R (quadratic) \u2014 "
             "power scales with the square",
    footer="R = 10 \u03a9    I_max = 10 A",
    single_panel=True,
)

R = 10.0
I_MAX = 10.0
I_OP = 6.0

i_full = np.linspace(0, I_MAX, 300)
p_full = power(i_full, R)

n_frames = 100
i_sweep = np.linspace(0, I_MAX, n_frames)
p_sweep = power(i_sweep, R)

fig.ax_hero.plot(i_full, i_full, color=fig.muted, linewidth=2, alpha=0.7,
                 label="I (linear reference)")
fig.ax_hero.plot(i_full, p_full, color=fig.accent, linewidth=2.5, zorder=3,
                 label="P = I\u00b2R")
fig.ax_hero.fill_between(i_full, i_full, p_full, color=fig.accent, alpha=0.08)

static_dot_linear = fig.ax_hero.scatter([I_OP], [I_OP], color=fig.muted, zorder=5, s=60)
static_dot_power = fig.ax_hero.scatter([I_OP], [power(I_OP, R)],
                                        color=fig.accent, zorder=5, s=60)
static_vline = fig.ax_hero.axvline(I_OP, color=fig.muted, linestyle="--",
                                    linewidth=1.2, alpha=0.5)

static_ann = fig.ax_hero.annotate(
    f"I = {I_OP:.1f} A    P = {power(I_OP, R):.0f} W",
    (I_OP, power(I_OP, R)), xytext=(25, -35),
    textcoords="offset points", color=fig.fg, fontsize=10,
    fontfamily=fig.font_mono,
    arrowprops=dict(arrowstyle="->", color=fig.muted))

fig.ax_hero.set_xlim(0, I_MAX)
fig.ax_hero.set_ylim(0, max(p_full) * 1.15)
fig.ax_hero.set_xlabel("Current (A)")
fig.ax_hero.set_ylabel("Value")
fig.ax_hero.set_title("Power scales with the square", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)
fig.ax_hero.legend(loc="upper left", fontsize=10)

fig.save("power_dissipation.png")

static_dot_linear.set_visible(False)
static_dot_power.set_visible(False)
static_vline.set_visible(False)
static_ann.set_visible(False)
static_ann.arrow_patch.set_visible(False)

linear_dot, = fig.ax_hero.plot([], [], "o", color=fig.muted, markersize=10,
                                markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
power_dot, = fig.ax_hero.plot([], [], "o", color=fig.accent, markersize=10,
                               markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
vline, = fig.ax_hero.plot([], [], color=fig.accent, linewidth=1,
                           linestyle="--", alpha=0.4)
label = fig.ax_hero.text(0.95, 0.95, "", color=fig.fg, fontsize=10,
                          fontfamily=fig.font_mono, ha="right", va="top",
                          transform=fig.ax_hero.transAxes)


def update(frame):
    i = i_sweep[frame]
    p = p_sweep[frame]

    linear_dot.set_data([i], [i])
    power_dot.set_data([i], [p])
    vline.set_data([i, i], [0, p])
    label.set_text(f"I = {i:.2f} A    P = {p:.0f} W")


fig.animate(n_frames, update, "power_dissipation.gif", fps=20)
