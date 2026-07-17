# EE & Math Visualisation Series — code.arts

Animated and static visual explanations of fundamental electrical engineering and mathematics concepts using matplotlib. Each topic follows a two-panel "Hero + Side" layout with a consistent dark theme.

## Topics

| Topic | Domain | Script | Output |
|---|---|---|---|
| Ohm's Law | EE | `scripts/ohms_law.py` | PNG + GIF |
| RC Time Constant | EE | `scripts/capacitor_rc.py` | GIF |
| RL Time Constant | EE | `scripts/inductor_rl.py` | GIF |
| Resonant Frequency | EE | `scripts/resonant_frequency.py` | GIF |
| Series vs Parallel | EE | `scripts/series_parallel.py` | PNG + GIF |
| Short Circuit | EE | `scripts/short_circuit.py` | PNG |
| Voltage Divider | EE | `scripts/voltage_divider.py` | GIF |
| Wire Resistance | EE | `scripts/wire_resistance.py` | PNG + GIF |
| Power Dissipation | EE | `scripts/power_dissipation.py` | PNG + GIF |
| AC Waveform | EE | `scripts/ac_waveform.py` | GIF |
| Slope-Intercept Form | Math | `scripts/slope_intercept.py` | PNG + GIF |

## Structure

```
├── physics/          # Pure computation, one module per topic
├── scripts/          # matplotlib figures and animations
├── outputs/          # Generated PNGs and GIFs
├── builder.py        # FigureBuilder — boilerplate reduction
├── theme.py          # Dark palette, header/footer helpers
├── animate.py        # FuncAnimation wrapper + GIF export
├── prompt.md         # Code generation template
├── pyproject.toml    # Project config & dependencies
└── Makefile          # Task runner
```

## Quick start

```sh
pip install -e .              # install project in dev mode
make all                      # regenerate all outputs
make topic/ohms_law           # run a single topic
make watch                    # auto-rebuild on file change
make clean                    # remove all outputs
```

## Creating a new topic

1. Add a computation module in `physics/<topic>.py` (pure numpy, no plotting)
2. Create a script in `scripts/<topic>.py` using `FigureBuilder`:

```python
from builder import FigureBuilder

fig = FigureBuilder(
    title="Topic Title",
    subtitle="One-liner explanation",
    footer="param=value  assumptions",
)

# Hero panel (left)
fig.ax_hero.plot(x, y, color=fig.accent, linewidth=2.5)
fig.ax_hero.set_xlabel("Label"); fig.ax_hero.set_ylabel("Label")
fig.ax_hero.grid(True, alpha=0.3)

# Side panel (right)
fig.ax_side.plot(x, y2, color=fig.series[1], linewidth=2.5)
fig.ax_side.set_title("Title", fontsize=11); fig.ax_side.grid(True, alpha=0.3)

fig.save("my_topic.png")              # static export
fig.animate(100, update_fn, "my_topic.gif")  # animated export
```

See `prompt.md` for the full template, or `scripts/sample.py` for a working example.

## Design

- **`physics/`** — pure functions (no plotting) for each concept
- **`FigureBuilder`** (`builder.py`) — creates the figure, grid, header, footer, handles save/animate/close. Dramatically reduces boilerplate (~35 lines per script vs ~130)
- **`theme.py`** — dark background (`#0a0a0a`), orange accent (`#d77600`), DM Mono / Inter fonts. Call via builder automatically
- **`animate.py`** — wraps `matplotlib.animation.FuncAnimation` with PillowWriter for GIF export

## Requirements

- Python ≥ 3.9
- `matplotlib`
- `numpy`
- `pillow` (for GIF export)

## Credits

Created by [code.arts](https://x.com/code_arts_).
