import os
from dataclasses import dataclass
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

import theme
from animate import make_animation, save_gif


@dataclass
class Tracker:
    dot: plt.Line2D
    vline: Optional[plt.Line2D] = None
    label: Optional[plt.Text] = None

    def update(self, x=None, y=None, text=None):
        if x is not None and y is not None:
            self.dot.set_data([x], [y])
        if x is not None and y is not None and self.vline is not None:
            self.vline.set_data([x, x], [0, y])
        if text is not None and self.label is not None:
            self.label.set_text(text)


class FigureBuilder:
    FIGWIDTH = 11
    FIGHEIGHT = 6.2
    LEFT = 0.06
    RIGHT = 0.97
    TOP = 0.82
    BOTTOM = 0.14
    WSPACE = 0.3

    def __init__(self, title, subtitle, footer=None, *, figsize=None, single_panel=False, layout="hero_side"):
        theme.apply()

        os.makedirs("outputs", exist_ok=True)

        if single_panel:
            layout = "single"

        self.layout = layout
        self._figsize = figsize

        if layout == "single":
            self._build_single()
        elif layout == "hero_side":
            self._build_hero_side()
        elif layout == "stacked":
            self._build_stacked()
        elif layout == "hero_stack":
            self._build_hero_stack()
        elif layout == "quad":
            self._build_quad()
        else:
            raise ValueError(f"Unknown layout: {layout}")

        theme.header(self.fig, title, subtitle)
        if footer:
            theme.footer(self.fig, footer)

    def _default_size(self, layout):
        return {
            "single": (7, 7),
            "hero_side": (11, 6.2),
            "stacked": (11, 6.2),
            "hero_stack": (13, 7.5),
            "quad": (12.5, 9),
        }[layout]

    def _build_single(self):
        w, h = self._figsize or self._default_size("single")
        self.fig = plt.figure(figsize=(w, h))
        self.gs = GridSpec(
            1, 1, figure=self.fig,
            left=0.10, right=0.95, top=0.80, bottom=0.12,
        )
        self.ax_hero = self.fig.add_subplot(self.gs[0, 0])
        self.ax_side = None

    def _build_hero_side(self):
        w, h = self._figsize or self._default_size("hero_side")
        self.fig = plt.figure(figsize=(w, h))
        self.gs = GridSpec(
            1, 2, figure=self.fig, width_ratios=[1.5, 1],
            left=self.LEFT, right=self.RIGHT, top=self.TOP,
            bottom=self.BOTTOM, wspace=self.WSPACE,
        )
        self.ax_hero = self.fig.add_subplot(self.gs[0, 0])
        self.ax_side = self.fig.add_subplot(self.gs[0, 1])

    def _build_stacked(self):
        w, h = self._figsize or self._default_size("stacked")
        self.fig = plt.figure(figsize=(w, h))
        self.gs = GridSpec(
            2, 1, figure=self.fig, height_ratios=[1, 1],
            left=0.08, right=0.95, top=self.TOP, bottom=0.10, hspace=0.35,
        )
        self.ax_hero = self.fig.add_subplot(self.gs[0, 0])
        self.ax_bottom = self.fig.add_subplot(self.gs[1, 0])
        self.ax_side = None

    def _build_hero_stack(self):
        w, h = self._figsize or self._default_size("hero_stack")
        self.fig = plt.figure(figsize=(w, h))
        self.gs = GridSpec(
            1, 2, figure=self.fig, width_ratios=[1.5, 1],
            left=self.LEFT, right=self.RIGHT, top=self.TOP,
            bottom=self.BOTTOM, wspace=self.WSPACE,
        )
        self.ax_hero = self.fig.add_subplot(self.gs[0, 0])
        inner = GridSpecFromSubplotSpec(
            2, 1, subplot_spec=self.gs[0, 1], hspace=0.35,
        )
        self.ax_top = self.fig.add_subplot(inner[0, 0])
        self.ax_bottom = self.fig.add_subplot(inner[1, 0])
        self.ax_side = None

    def _build_quad(self):
        w, h = self._figsize or self._default_size("quad")
        self.fig = plt.figure(figsize=(w, h))
        self.gs = GridSpec(
            2, 2, figure=self.fig,
            left=0.07, right=0.96, top=self.TOP, bottom=0.10,
            wspace=0.28, hspace=0.35,
        )
        self.ax_tl = self.fig.add_subplot(self.gs[0, 0])
        self.ax_tr = self.fig.add_subplot(self.gs[0, 1])
        self.ax_bl = self.fig.add_subplot(self.gs[1, 0])
        self.ax_br = self.fig.add_subplot(self.gs[1, 1])
        self.ax_hero = self.ax_tl
        self.ax_side = self.ax_tr

    @property
    def accent(self):
        return theme.ACCENT

    @property
    def muted(self):
        return theme.MUTED

    @property
    def fg(self):
        return theme.FG

    @property
    def bg(self):
        return theme.BG

    @property
    def grid(self):
        return theme.GRID

    @property
    def series(self):
        return theme.SERIES

    @property
    def font_mono(self):
        return theme.FONT_MONO

    @property
    def font_sans(self):
        return theme.FONT_SANS

    def add_callout(self, ax, x, y, text):
        ax.scatter([x], [y], color=self.accent, zorder=5, s=60)
        ax.annotate(
            text, (x, y),
            xytext=(10, -30), textcoords="offset points",
            color=self.fg, fontsize=9, fontfamily=self.font_mono,
            bbox=dict(boxstyle="round,pad=0.3", facecolor=self.bg,
                      edgecolor=self.muted, linewidth=0.5),
            arrowprops=dict(arrowstyle="->", color=self.muted, lw=0.8),
        )

    def add_threshold(self, ax, value, axis, label=None):
        if axis == "y":
            ax.axhline(value, color=self.muted, linestyle="--",
                       linewidth=1.2, alpha=0.7)
            if label:
                xlim = ax.get_xlim()
                ax.text(xlim[1], value, f"  {label}", color=self.muted,
                        fontsize=8, fontfamily=self.font_mono, va="center")
        elif axis == "x":
            ax.axvline(value, color=self.muted, linestyle="--",
                       linewidth=1.2, alpha=0.7)
            if label:
                ylim = ax.get_ylim()
                ax.text(value, ylim[1], f"{label}  ", color=self.muted,
                        fontsize=8, fontfamily=self.font_mono, ha="right", va="bottom")

    def add_event_marker(self, ax, x, y, label=None):
        ax.scatter([x], [y], marker="*", color=self.accent, s=120,
                   edgecolor=self.fg, linewidth=0.8, zorder=6)
        if label:
            ax.annotate(
                label, (x, y),
                xytext=(0, 20), textcoords="offset points",
                ha="center", va="bottom",
                color=self.fg, fontsize=9, fontfamily=self.font_mono,
                arrowprops=dict(arrowstyle="->", color=self.muted, lw=0.8),
            )

    def add_tracker(self, ax, color, *, use_vline=True, label_pos="tr"):
        label_anchors = {
            "tr": (0.95, 0.95, "right", "top"),
            "tl": (0.05, 0.95, "left", "top"),
            "bl": (0.05, 0.05, "left", "bottom"),
            "br": (0.95, 0.05, "right", "bottom"),
        }
        x, y, ha, va = label_anchors.get(label_pos, label_anchors["tr"])

        dot, = ax.plot([], [], "o", color=color, markersize=10,
                        markeredgecolor=self.fg, markeredgewidth=1.5, zorder=10)
        vline = None
        if use_vline:
            vline, = ax.plot([], [], color=color, linewidth=1,
                              linestyle="--", alpha=0.4)
        label = ax.text(x, y, "", color=self.fg, fontsize=10,
                         fontfamily=self.font_mono, ha=ha, va=va,
                         transform=ax.transAxes)
        return Tracker(dot=dot, vline=vline, label=label)

    @staticmethod
    def hide(*artists):
        for a in artists:
            if a is None:
                continue
            a.set_visible(False)
            if hasattr(a, "arrow_patch") and a.arrow_patch is not None:
                a.arrow_patch.set_visible(False)

    def setup_axis(self, ax, *, xlim=None, ylim=None, xlabel=None, ylabel=None,
                   title=None, title_fontsize=11, grid=True, grid_alpha=0.3):
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
        if title is not None:
            ax.set_title(title, fontsize=title_fontsize)
        if grid:
            ax.grid(True, alpha=grid_alpha)

    def save(self, path, dpi=150):
        path = os.path.join("outputs", path) if not path.startswith("outputs/") else path
        self.fig.savefig(path, dpi=dpi)
        print(f"saved {path}")

    def animate(self, n_frames, update_fn, path, fps=20):
        anim = make_animation(self.fig, update_fn, n_frames, fps=fps)
        path = os.path.join("outputs", path) if not path.startswith("outputs/") else path
        save_gif(anim, path, fps=fps)
        plt.close(self.fig)
        return anim

    def close(self):
        plt.close(self.fig)
