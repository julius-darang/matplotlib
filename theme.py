"""
theme.py
Central brand config. Every figure in the series imports from here so
a palette/font tweak propagates to every topic (short circuit, power
flow, out-of-step, hosting capacity, ...) at once.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl

# --- code.arts palette --------------------------------------------------
BG        = "#0a0a0a"   # near-black canvas
FG        = "#f5f5f4"   # near-white text
ACCENT    = "#d77600"   # signature orange — use ONLY for the "answer"
GRID      = "#2a2a2a"   # faint gridlines / separators
MUTED     = "#7a7a78"   # secondary annotations, footer text
SERIES    = ["#d77600", "#4a90d9", "#5fb87a", "#c85c5c"]  # multi-curve fallback

FONT_MONO = "DM Mono"
FONT_SANS = "Inter"


def apply():
    """Call once at the top of any script before creating figures."""
    mpl.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor":   BG,
        "savefig.facecolor": BG,
        "axes.edgecolor":   GRID,
        "axes.labelcolor":  FG,
        "text.color":       FG,
        "xtick.color":      MUTED,
        "ytick.color":      MUTED,
        "grid.color":       GRID,
        "grid.linewidth":   0.6,
        "font.family":      FONT_SANS,
        "axes.titlesize":   13,
        "axes.titleweight": "bold",
        "axes.spines.top":  False,
        "axes.spines.right": False,
    })


def header(fig, title, subtitle):
    fig.text(0.03, 0.96, title, fontsize=20, fontweight="bold",
              color=FG, fontfamily=FONT_SANS)
    fig.text(0.03, 0.925, subtitle, fontsize=11, color=MUTED,
              fontfamily=FONT_SANS)


def footer(fig, assumptions, handle="code.arts"):
    fig.text(0.03, 0.015, assumptions, fontsize=8, color=MUTED,
              fontfamily=FONT_MONO)
    fig.text(0.97, 0.015, handle, fontsize=9, color=ACCENT,
              fontfamily=FONT_MONO, ha="right")