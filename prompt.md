# Code Generation Template for EE & Math Visualisation Series

## Directory structure

```
physics/<topic>.py   — pure computation (no matplotlib). One function per concept.
scripts/<topic>.py   — matplotlib figure using FigureBuilder. ~35 lines typical.
outputs/<topic>.png  /  outputs/<topic>.gif
```

## Quick reference

physics module — pure numpy functions only, NO plotting:

```python
import numpy as np

def my_func(t, param):
    return np.something(t, param)
```

script — use the FigureBuilder:

```python
import numpy as np
from builder import FigureBuilder
from physics.my_topic import my_func

# ALL styling, layout, header, footer, and output dir are handled by the builder.
fig = FigureBuilder(
    title="Topic Title",
    subtitle="One-liner explaining the concept",
    footer="param1=...  param2=...  assumptions note",
)

# Precompute data
x = np.linspace(0, 10, 300)
y = my_func(x, ...)

# Hero panel (left, wider) — main visualization
fig.ax_hero.plot(x, y, color=fig.accent, linewidth=2.5)
fig.ax_hero.fill_between(x, y, color=fig.accent, alpha=0.08)
fig.ax_hero.set_xlabel("Label")
fig.ax_hero.set_ylabel("Label")
fig.ax_hero.set_title("Descriptive title", fontsize=11)
fig.ax_hero.grid(True, alpha=0.3)

# Side panel (right) — supporting visualization
fig.ax_side.plot(x, y_secondary, color=fig.series[1], linewidth=2.5)
fig.ax_side.set_title("Descriptive title", fontsize=11)
fig.ax_side.set_xlabel("Label")
fig.ax_side.grid(True, alpha=0.3)

# Static export
fig.save("my_topic.png")
# optionally fig.save("my_topic.pdf", dpi=300)

# Animation (optional):
# ... define animated artists via fig.ax_hero.plot([], [], ...) etc.
# def update(frame):
#     t = t_sweep[frame]
#     animated_artist.set_data([t], [y_sweep[frame]])
# fig.animate(100, update, "my_topic.gif", fps=20)
```

## Color rules
- `fig.accent` (orange `#d77600`) — primary curve / "the answer"
- `fig.series[1]` (blue `#4a90d9`) — secondary curve
- `fig.series[2]` (green `#5fb87a`) — tertiary (rare)
- `fig.muted` (gray `#7a7a78`) — reference curves, annotations, dashed lines
- `fig.fg` (white `#f5f5f4`) — labels, text
- `fig.bg` (near-black `#0a0a0a`) — canvas
- `fig.grid` (dark gray `#2a2a2a`) — grid lines

## Layout specs
- Figure: 11 x 6.2 inches (default)
- GridSpec: 1x2, width_ratios=[1.5, 1], margins: left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3
- Fonts: Inter (sans) for headers/labels, DM Mono (mono) for data values
- No top/right spines (set in theme)
- Grid alpha: 0.3
- DPI: 150 for PNG, 20 fps for GIF, 100 frames typical

## Animation pattern
- Precompute full-resolution curves for static and downsampled sweeps for animation
- Create empty animated artists BEFORE the update function: `.plot([], [], ...)`
- Update artists **in place** in the update function (no ax.clear() or ax.plot() per frame)
- Hide static markers with `.set_visible(False)` if they'd overlap with animated ones

## Naming
- physics/functions: snake_case, descriptive (e.g. `v_charge`, `fault_current_profile`)
- script files: snake_case matching the topic (e.g. `ac_waveform.py`)
- output files: same name as script (e.g. `ac_waveform.png`, `ac_waveform.gif`)
- Constants at top of scripts: UPPER_SNAKE_CASE (e.g. `V_SOURCE = 5.0`)
