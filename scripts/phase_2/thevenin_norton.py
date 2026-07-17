import os
import tempfile
import numpy as np
from matplotlib.image import imread
from lcapy import Circuit
from lcapy.schemmisc import Pos
import warnings

from builder import FigureBuilder
from physics.phase_2.thevenin_norton import (
    thevenin_voltage, thevenin_resistance, norton_current,
    load_voltage, load_current,
)

warnings.filterwarnings("ignore", "FigureCanvasAgg is non-interactive")

V_SOURCE = 12.0
R1 = 4.0
R2 = 6.0

V_TH = thevenin_voltage(V_SOURCE, R1, R2)
R_TH = thevenin_resistance(R1, R2)
I_N = norton_current(V_TH, R_TH)
I_SC = I_N

R_LOAD_MIN = 0.5
R_LOAD_MAX = 20.0
N_FRAMES = 100

r_load_sweep = np.linspace(R_LOAD_MIN, R_LOAD_MAX, N_FRAMES)
v_load_sweep = load_voltage(V_TH, R_TH, r_load_sweep)
i_load_sweep = load_current(V_TH, R_TH, r_load_sweep)

fig = FigureBuilder(
    title="Three circuits, one operating point",
    subtitle="Thevenin and Norton equivalents match the original at every load",
    footer="V=12V  R1=4\u03a9  R2=6\u03a9  V_th=7.2V  R_th=2.4\u03a9  I_n=3A  ideal DC circuit",
    layout="quad",
)


def _draw_circuit(netlist, node_positions, scale=2):
    sch = tempfile.NamedTemporaryFile(suffix=".sch", mode="w", delete=False)
    sch.write(netlist)
    sch.close()
    cct = Circuit(sch.name)
    cct.sch.node_positions = node_positions
    out = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    out.close()
    try:
        cct.draw(out.name, scale=scale, method="lineq")
        img = imread(out.name)
    finally:
        os.unlink(sch.name)
        os.unlink(out.name)
    return img


def _display_circuit(ax, img):
    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines[:].set_visible(False)


RLOAD_LABEL = "R_load = {:.1f}\u03a9"

# --- Original circuit (top-left) ---
orig_nodes = {
    "1": Pos(0, 3),
    "2": Pos(2, 3),
    "0": Pos(0, 0),
    "0_2": Pos(2, 0),
}
orig_net = (
    "V 1 0 12; down, color=gray\n"
    "R1 1 2 4; right, color=gray\n"
    "R2 2 0 6; down, color=gray\n"
    "W 0 0_2; right\n"
)
orig_img = _draw_circuit(orig_net, orig_nodes)
_display_circuit(fig.ax_tl, orig_img)
r_load_label_tl = fig.ax_tl.text(
    0.5, -0.08, RLOAD_LABEL.format(r_load_sweep[0]),
    color=fig.fg, fontsize=9, fontfamily=fig.font_mono,
    ha="center", va="top", transform=fig.ax_tl.transAxes,
)

# --- Thevenin equivalent (top-right) ---
th_nodes = {
    "1": Pos(0, 3),
    "2": Pos(2, 3),
    "0": Pos(0, 0),
    "0_2": Pos(2, 0),
}
th_net = (
    f"Vth 1 0 {V_TH:.1f}; down, color=orange\n"
    f"Rth 1 2 {R_TH:.1f}; right, color=orange\n"
    "W 2 0_2; down\n"
    "W 0 0_2; right\n"
)
th_img = _draw_circuit(th_net, th_nodes)
_display_circuit(fig.ax_tr, th_img)
r_load_label_tr = fig.ax_tr.text(
    0.5, -0.08, RLOAD_LABEL.format(r_load_sweep[0]),
    color=fig.fg, fontsize=9, fontfamily=fig.font_mono,
    ha="center", va="top", transform=fig.ax_tr.transAxes,
)

# --- Norton equivalent (bottom-left) ---
nor_nodes = {
    "1": Pos(0, 3),
    "0": Pos(0, 0),
    "0_2": Pos(2, 0),
    "0_3": Pos(2, 3),
}
nor_net = (
    f"In 1 0 {I_N:.1f}; down, color=blue\n"
    f"Rth 1 0 {R_TH:.1f}; right, color=blue\n"
    "W 0 0_2; right\n"
)
nor_img = _draw_circuit(nor_net, nor_nodes)
_display_circuit(fig.ax_bl, nor_img)
r_load_label_bl = fig.ax_bl.text(
    0.5, -0.08, RLOAD_LABEL.format(r_load_sweep[0]),
    color=fig.fg, fontsize=9, fontfamily=fig.font_mono,
    ha="center", va="top", transform=fig.ax_bl.transAxes,
)

ax_titles = {
    fig.ax_tl: "Original circuit",
    fig.ax_tr: "Thevenin equivalent",
    fig.ax_bl: "Norton equivalent",
}
for ax, title in ax_titles.items():
    ax.set_title(title, fontsize=11, color=fig.fg, pad=8)

# --- V-I panel (bottom-right) ---
vi_max_i = I_SC * 1.15
vi_max_v = V_TH * 1.15
fig.ax_br.set_xlim(0, vi_max_i)
fig.ax_br.set_ylim(0, vi_max_v)
fig.ax_br.set_xlabel("Current (A)")
fig.ax_br.set_ylabel("Voltage (V)")
fig.ax_br.set_title("V-I plane: identical source characteristic for all three",
                     fontsize=11)
fig.ax_br.grid(True, alpha=0.3)

source_line, = fig.ax_br.plot(
    [0, I_SC], [V_TH, 0], color=fig.accent, linewidth=2.5, zorder=2,
)
fig.ax_br.text(
    I_SC * 0.45, V_TH * 0.55, "Source\ncharacteristic",
    color=fig.accent, fontsize=8, fontfamily=fig.font_mono,
    ha="center", va="center", alpha=0.8,
)

load_line, = fig.ax_br.plot(
    [0, i_load_sweep[0]], [0, v_load_sweep[0]],
    color=fig.series[1], linewidth=2, linestyle="--", zorder=3,
)

intersection = fig.ax_br.scatter(
    [i_load_sweep[0]], [v_load_sweep[0]],
    marker="*", color=fig.accent, s=150,
    edgecolor=fig.fg, linewidth=0.8, zorder=10,
)

v_line, = fig.ax_br.plot(
    [i_load_sweep[0], i_load_sweep[0]], [0, v_load_sweep[0]],
    color=fig.muted, linewidth=1, linestyle=":", zorder=1,
)
i_line, = fig.ax_br.plot(
    [0, i_load_sweep[0]], [v_load_sweep[0], v_load_sweep[0]],
    color=fig.muted, linewidth=1, linestyle=":", zorder=1,
)

v_label = fig.ax_br.text(
    i_load_sweep[0] + 0.02, v_load_sweep[0] / 2,
    f"V_load = {v_load_sweep[0]:.2f} V",
    color=fig.fg, fontsize=8, fontfamily=fig.font_mono, va="center",
)
i_label = fig.ax_br.text(
    i_load_sweep[0] / 2, v_load_sweep[0] + 0.02,
    f"I_load = {i_load_sweep[0]:.2f} A",
    color=fig.fg, fontsize=8, fontfamily=fig.font_mono, ha="center",
)
r_label = fig.ax_br.text(
    0.95, 0.95, RLOAD_LABEL.format(r_load_sweep[0]),
    color=fig.fg, fontsize=9, fontfamily=fig.font_mono,
    ha="right", va="top", transform=fig.ax_br.transAxes,
)


def update(frame):
    rl = r_load_sweep[frame]
    vl = v_load_sweep[frame]
    il = i_load_sweep[frame]

    r_load_label_tl.set_text(RLOAD_LABEL.format(rl))
    r_load_label_tr.set_text(RLOAD_LABEL.format(rl))
    r_load_label_bl.set_text(RLOAD_LABEL.format(rl))

    load_line.set_data([0, il], [0, vl])
    intersection.set_offsets([[il, vl]])
    v_line.set_data([il, il], [0, vl])
    i_line.set_data([0, il], [vl, vl])

    v_label.set_position((il + 0.02, vl / 2))
    v_label.set_text(f"V_load = {vl:.2f} V")
    i_label.set_position((il / 2, vl + 0.02))
    i_label.set_text(f"I_load = {il:.2f} A")
    r_label.set_text(RLOAD_LABEL.format(rl))


fig.animate(N_FRAMES, update, "thevenin_norton.gif", fps=20)
