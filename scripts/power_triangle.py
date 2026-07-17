import numpy as np
from matplotlib.patches import Polygon
from builder import FigureBuilder
from physics.power_triangle import power_triangle, s_vs_pf

P = 100.0
n_frames = 100
PF_sweep = np.linspace(1.0, 0.6, n_frames)

PF_full, S_full = s_vs_pf(P)

fig = FigureBuilder(
    title="Reactive Power Opens the Triangle",
    subtitle=(
        "As power factor falls, apparent power S must grow "
        "to deliver the same real power P"
    ),
    footer=(
        "P = 100 kW fixed  PF = cos(\u03b8)  "
        "S = P / PF  Q = \u221a(S\u00b2 \u2212 P\u00b2)"
    ),
)

# ========== Hero panel ==========
ax = fig.ax_hero
ymax = P * np.tan(np.arccos(0.6)) * 1.18
ax.set_xlim(0, P * 1.18)
ax.set_ylim(0, ymax)
ax.set_aspect("equal")
ax.set_xlabel("Real Power P (kW)")
ax.set_ylabel("Reactive Power Q (kVAR)")
ax.set_title("Power Triangle at Two Power Factors", fontsize=11)
ax.grid(True, alpha=0.3)

# Shared P leg (horizontal)
ax.plot([0, P], [0, 0], color=fig.muted, linewidth=2.5, alpha=0.8, zorder=3)
ax.text(P / 2, -ymax * 0.04, "P (Real Power)", color=fig.muted,
        fontsize=8, ha="center", fontfamily=fig.font_mono)

# Muted reference: PF=1.0 degenerate triangle
ax.plot([P], [0], "o", color=fig.muted, markersize=9,
        markeredgecolor=fig.fg, markeredgewidth=0.8, zorder=5)
ax.annotate(
    f"PF = 1.0\nP = S = {P:.0f} kW\nQ = 0 kVAR",
    (P, 0),
    xytext=(10, -30),
    textcoords="offset points",
    color=fig.fg, fontsize=9, fontfamily=fig.font_mono,
    bbox=dict(boxstyle="round,pad=0.3", facecolor=fig.bg,
              edgecolor=fig.muted, linewidth=0.5),
    arrowprops=dict(arrowstyle="->", color=fig.muted, lw=0.8),
)

# ========== Side panel ==========
axs = fig.ax_side
axs.set_xlim(0.55, 1.05)
axs.set_ylim(P * 0.85, P / 0.55)
axs.set_xlabel("Power Factor")
axs.set_ylabel("Apparent Power S (kVA)")
axs.set_title("Apparent Power Swells as PF Falls", fontsize=11)
axs.grid(True, alpha=0.3)

axs.plot(PF_full, S_full, color=fig.series[1], linewidth=2.5)
axs.fill_between(PF_full, S_full, P, color=fig.series[1], alpha=0.08)
axs.axhline(P, color=fig.muted, linestyle="--", linewidth=1, alpha=0.5)
axs.text(0.57, P + 3, "P (Real Power)", color=fig.muted, fontsize=7,
         fontfamily=fig.font_mono, va="bottom")

fig.add_event_marker(axs, 1.0, P, label="PF = 1.0")

fig.save("power_triangle.png")

# ========== Animated artists ==========
# Hero: accent triangle fill
accent_fill = Polygon([[0, 0], [P, 0], [P, 0]], closed=True,
                      color=fig.accent, alpha=0.15, zorder=2)
ax.add_patch(accent_fill)

# Hero: accent triangle edges
accent_q, = ax.plot([], [], color=fig.accent, linewidth=2.5, zorder=4)
accent_hyp, = ax.plot([], [], color=fig.accent, linewidth=2.5, zorder=4)

# Hero: animated callout
accent_dot, = ax.plot([], [], "o", color=fig.accent, markersize=10,
                       markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
accent_ann = ax.annotate("", (0, 0), xytext=(15, -25),
                          textcoords="offset points",
                          color=fig.fg, fontsize=9, fontfamily=fig.font_mono,
                          bbox=dict(boxstyle="round,pad=0.3",
                                    facecolor=fig.bg,
                                    edgecolor=fig.accent, linewidth=0.5),
                          arrowprops=dict(arrowstyle="->",
                                          color=fig.muted, lw=0.8))

# Side: animated dot and label
side_dot, = axs.plot([], [], "o", color=fig.accent, markersize=10,
                      markeredgecolor=fig.fg, markeredgewidth=1.5, zorder=10)
side_vline, = axs.plot([], [], color=fig.accent, linewidth=1,
                        linestyle="--", alpha=0.4)
side_label = axs.text(0.05, 0.95, "", color=fig.fg, fontsize=9,
                       fontfamily=fig.font_mono, ha="left", va="top",
                       transform=axs.transAxes)


def update(frame):
    pf = PF_sweep[frame]
    _, q, s = power_triangle(P, pf)

    verts = np.array([[0, 0], [P, 0], [P, q]])
    accent_fill.set_xy(verts)
    accent_q.set_data([P, P], [0, q])
    accent_hyp.set_data([0, P], [0, q])

    accent_dot.set_data([P], [q])
    accent_ann.xy = (P, q)
    accent_ann.set_text(
        f"PF = {pf:.2f}\n"
        f"P = {P:.0f} kW\n"
        f"Q = {q:.0f} kVAR\n"
        f"S = {s:.0f} kVA"
    )

    side_dot.set_data([pf], [s])
    side_vline.set_data([pf, pf], [0, s])
    side_label.set_text(f"PF = {pf:.2f}\nS = {s:.0f} kVA")


fig.animate(n_frames, update, "power_triangle.gif", fps=20)
