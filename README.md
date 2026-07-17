# EE & Math Visualisation Series — code.arts

Animated and static visual explanations of fundamental electrical engineering and mathematics concepts using matplotlib. Dark-themed, annotation-light, idea-first.

## Architecture

```
├── physics/           # Pure numpy computation, one module per topic
│   ├── phase_1/       #   Foundational topics
│   │   └── <topic>.py #     Returns raw numbers/arrays — no plotting, no formatting
│   └── phase_2/       #   Advanced topics (work in progress)
│       └── <topic>.py
├── scripts/           # Matplotlib figures using FigureBuilder
│   ├── phase_1/       #   Foundational topic scripts
│   │   └── <topic>.py #     ~35-45 lines typical
│   └── phase_2/       #   Advanced topic scripts
│       └── <topic>.py
├── outputs/           # Generated PNGs and GIFs
│   ├── phase_1/       #   Outputs for foundational topics
│   │   ├── <topic>.png
│   │   └── <topic>.gif
│   └── phase_2/       #   Outputs for advanced topics
│       ├── <topic>.png
│       └── <topic>.gif
├── builder.py         # FigureBuilder — layout, theme, annotation helpers, save/animate
├── theme.py           # Dark palette (bg/fg/accent/series/muted), font config, header/footer
├── animate.py         # FuncAnimation wrapper + PillowWriter GIF export
├── design.md          # Full design spec and code generation template
├── pyproject.toml     # Project config & dependencies
└── Makefile           # Task runner
```

## Design pattern

**Separation of concerns:**
- `physics/phase_<N>/<topic>.py` — pure numpy functions only. Take parameters, return arrays. No matplotlib imports.
- `scripts/phase_<N>/<topic>.py` — create a `FigureBuilder`, precompute data, plot, annotate, export. The builder handles all styling, layout, header, footer, and output directory.
- Annotations use builder methods (`add_callout`, `add_threshold`, `add_event_marker`) — at most one of each per panel.

**Layout classes** (defined in `builder.py`):
| Class | Panels | Figure | Use case |
|---|---|---|---|
| `SinglePanel` | 1 | 7×7" | Single self-contained relationship |
| `HeroAndSide` | 2 (1×2) | 11×6.2" | Hero + one supporting/consequence view |
| `StackedPair` | 2 (2×1) | 11×6.2" | Same x-axis, before/after or charge/discharge |
| `HeroAndStack` | 3 (1×2, nested) | 13×7.5" | Hero + two side views on different clocks |
| `QuadPanel` | 4 (2×2) | 12.5×9" | Four roughly equal comparison views |

**Animation** — precompute all data upfront, create empty artists, update in place via `set_data`/`set_offsets`/`set_text`. No `ax.clear()` or re-plotting per frame.

## Title & narrative discipline

- `title=` states the surprising claim the animation proves, not the topic's textbook name (e.g. "why fault current falls off," not "Short Circuit Current").
- `subtitle=` states the mechanism in one line.
- `footer=` states the numeric assumptions that make the model a simplification.

## Quick start

```sh
pip install -e .              # install project in dev mode
make all                      # regenerate all outputs
make topic/phase_1/ohms_law   # run a single topic (phase_1 or phase_2)
make watch                    # auto-rebuild on file change
make clean                    # remove all outputs
```

## Creating a new topic

1. Add a computation module in `physics/phase_<N>/<topic>.py` (pure numpy, no plotting)
2. Create a script in `scripts/phase_<N>/<topic>.py` using `FigureBuilder`:

```python
from builder import FigureBuilder

fig = FigureBuilder(
    title="The surprising claim, not the topic name",
    subtitle="One-liner explaining the mechanism",
    footer="param1=...  param2=...  assumptions note",
)

# Precompute data
x = np.linspace(0, 10, 300)
y = my_func(x, ...)

# Hero panel (left, wider)
fig.ax_hero.plot(x, y, color=fig.accent, linewidth=2.5)
fig.ax_hero.fill_between(x, y, color=fig.accent, alpha=0.08)
fig.ax_hero.set_xlabel("Label")
fig.ax_hero.set_ylabel("Label")
fig.ax_hero.set_title("Descriptive title", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

# Annotation layer
fig.add_callout(fig.ax_hero, x0, y0, f"τ={tau:.2f}s  63% at t={tau:.2f}s")
fig.add_threshold(fig.ax_hero, value=limit, axis="y", label="insulation limit")
fig.add_event_marker(fig.ax_hero, x0, y0, label="breakdown")

# Side panel (right)
fig.ax_side.plot(x, y_secondary, color=fig.series[1], linewidth=2.5)
fig.ax_side.set_title("Descriptive title", fontsize=11)
fig.ax_side.grid(True, alpha=0.3)

fig.save("my_topic.png")
# fig.animate(100, update_fn, "my_topic.gif", fps=20)
```

See `design.md` for the full spec and production pipeline.

## Requirements

- Python ≥ 3.9
- `matplotlib`
- `numpy`
- `pillow` (for GIF export)

## Credits

Created by [code.arts](https://x.com/code_arts_).
