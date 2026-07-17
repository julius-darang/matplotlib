import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import theme
from animate import make_animation, save_gif


class FigureBuilder:
    FIGWIDTH = 11
    FIGHEIGHT = 6.2
    LEFT = 0.06
    RIGHT = 0.97
    TOP = 0.82
    BOTTOM = 0.14
    WSPACE = 0.3

    def __init__(self, title, subtitle, footer=None, *, figsize=None, single_panel=False):
        theme.apply()

        os.makedirs("outputs", exist_ok=True)

        w, h = figsize or (self.FIGWIDTH, self.FIGHEIGHT)
        self.fig = plt.figure(figsize=(w, h))

        if single_panel:
            self.gs = GridSpec(
                1, 1, figure=self.fig,
                left=0.08, right=0.97, top=self.TOP, bottom=self.BOTTOM,
            )
            self.ax_hero = self.fig.add_subplot(self.gs[0, 0])
            self.ax_side = None
        else:
            self.gs = GridSpec(
                1, 2, figure=self.fig, width_ratios=[1.5, 1],
                left=self.LEFT, right=self.RIGHT, top=self.TOP,
                bottom=self.BOTTOM, wspace=self.WSPACE,
            )
            self.ax_hero = self.fig.add_subplot(self.gs[0, 0])
            self.ax_side = self.fig.add_subplot(self.gs[0, 1])

        theme.header(self.fig, title, subtitle)
        if footer:
            theme.footer(self.fig, footer)

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
