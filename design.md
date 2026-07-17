# Visualization Process with Matplotlib

## Directory structure

```
physics/<topic>.py   — pure computation (no matplotlib). One function per concept.
scripts/<topic>.py   — matplotlib figure using FigureBuilder. ~35-45 lines typical.
outputs/<topic>.png  /  outputs/<topic>.gif
```

## Quick reference

physics module — pure numpy functions only, NO plotting. Return raw numbers/arrays only — any string formatting for callouts happens in the script, not here.

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
    title="The surprising claim, not the topic name",   # e.g. "why the gap widens"
    subtitle="One-liner explaining the mechanism",
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

# Annotation layer — numbers always derived from physics output, never hardcoded
fig.add_callout(fig.ax_hero, x0, y0, f"τ={tau:.2f}s  63% at t={tau:.2f}s")
fig.add_threshold(fig.ax_hero, value=limit, axis="y", label="insulation limit")
fig.add_event_marker(fig.ax_hero, x0, y0, label="breakdown")

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

## Annotation helpers (builder methods)
- `fig.add_callout(ax, x, y, text)` — boxed monospace readout at a data point; text is always an f-string built from physics output, e.g. `f"grid pf = {pf:.3f} LEADING"`.
- `fig.add_threshold(ax, value, axis, label=None)` — dashed gray limit/crossover line (axhline or axvline) with an optional right-aligned label.
- `fig.add_event_marker(ax, x, y, label=None)` — single star/dot marker at the critical point, with an optional arrow-annotated label offset from it.
- Use at most one callout + one threshold + one event marker per panel — more than that clutters the "why" instead of clarifying it.

## Color rules
- `fig.accent` (orange `#d77600`) — primary curve / "the answer" / the thing being explained.
- `fig.series[1]` (blue `#4a90d9`) — secondary curve or comparison quantity.
- `fig.series[2]` (green `#5fb87a`) — tertiary curve, used sparingly.
- `fig.muted` (gray `#7a7a78`) — reference/ideal curves, threshold lines, dashed annotations.
- `fig.fg` (white `#f5f5f4`) — labels, callout text, event marker edges.
- `fig.bg` (near-black `#0a0a0a`) — canvas and callout box fill.
- `fig.grid` (dark gray `#2a2a2a`) — grid lines.
- Keep color-to-role mapping identical across every panel in a figure so one legend teaches the whole piece.

## Layout specs

Shared across all layouts: Inter (sans) for headers/labels, DM Mono (mono) for data values and callout text; no top/right spines; grid alpha 0.3; DPI 150 for PNG, 20 fps / 100 frames typical for GIF.

### 1 panel — `SinglePanel`
- Figure: 7 x 7 inches (1:1 ratio) — used for a single self-contained relationship with no side comparison (e.g. unit circle, a single sweeping curve).
- GridSpec: 1x1, margins: left=0.10, right=0.95, top=0.80, bottom=0.12.

### 2 panels — `HeroAndSide`
- Figure: 11 x 6.2 inches (current default).
- GridSpec: 1x2, width_ratios=[1.5, 1], margins: left=0.06, right=0.97, top=0.82, bottom=0.14, wspace=0.3.
- Use when one hero relationship needs a single supporting/consequence view.

### 2 panels — `StackedPair`
- Figure: 11 x 6.2 inches (current default).
- GridSpec: 2x1, height_ratios=[1,1], margins: left=0.08, right=0.95, top=0.82, bottom=0.10, hspace=0.35.
- Use when both panels share the same x-axis (e.g. charge vs discharge, before/after).

### 3 panels — `HeroAndStack`
- Figure: 13 x 7.5 inches (current default).
- GridSpec: 1x2 outer (width_ratios=[1.5, 1]), right column split via nested 2x1 subgridspec (hspace=0.35); hero margins as `HeroAndSide`.
- Use when the hero panel needs two side views on different clocks/frames (e.g. phasor + time-domain, or event + downstream consequence).

### 3-4 panels — `QuadPanel`
- Figure: 12.5 x 9 inches (current default), or 11 x 8 inches if labels feel cramped.
- GridSpec: 2x2, margins: left=0.07, right=0.96, top=0.82, bottom=0.10, wspace=0.28, hspace=0.35.
- Use only when no single panel is clearly dominant — four roughly equal comparison views.

Only add a new layout class beyond these five when a topic genuinely can't fit — don't build ahead of need.

## Animation pattern
- Precompute full-resolution curves for static export and a downsampled sweep array for animation frames.
- Create empty animated artists BEFORE the update function: `.plot([], [], ...)` or `.scatter([], [])`.
- Update artists **in place** in the update function (`.set_data`, `.set_offsets`, `.set_text`) — no `ax.clear()` or re-plotting per frame.
- If a callout box shows a live value, update it via `.set_text()` in the same update function rather than redrawing it.
- Hide static markers with `.set_visible(False)` if they'd overlap with animated ones.

## Naming
- physics/functions: snake_case, descriptive (e.g. `v_charge`, `fault_current_profile`).
- script files: snake_case matching the topic (e.g. `ac_waveform.py`).
- output files: same name as script (e.g. `ac_waveform.png`, `ac_waveform.gif`).
- Constants at top of scripts: UPPER_SNAKE_CASE (e.g. `V_SOURCE = 5.0`).

## Title & narrative discipline
- `title=` states the surprising claim the animation proves, not the topic's textbook name (e.g. "why fault current falls off," not "Short Circuit Current").
- `subtitle=` states the mechanism in one line; `footer=` states the numeric assumptions that make the model a simplification, stated plainly rather than apologetically.

## Idea-to-visual production pipeline

Two starting points feed the same pipeline from step 2 onward:
- **A. Raw technical idea** — a phenomenon or edge case worth explaining (e.g. out-of-step relay tripping); step 1 does real work here.
- **B. Textbook fact** — a known relationship being taught (e.g. RC charge/discharge); step 1 is about *finding the counterintuitive angle inside it*, not inventing a new claim.

1. **Frame as a counterintuitive claim** — for (A), state the surprising behavior directly as the title; for (B), find the sharpest "wait, what?" angle the fact already contains (e.g. not "RC time constant" but "same τ governs both charge and discharge"). Either way, the title is the hook sentence, not the topic name.
2. **Reduce to the minimal idealized model, and say so out loud** — footer names the simplification explicitly ("lossless line," "idealized 2-wire motor") as a credibility move, not a hedge.
3. **Hero panel sweeps the full domain; side panel(s) show the consequence or an alternate view** — same event in a different coordinate frame (phasor vs time) or its downstream cost (temp curve, component bar chart).
4. **Mark the threshold, not just the curve** — dashed limit lines, shaded regions past a critical value, one highlighted marker at the exact moment things go wrong.
5. **Anchor with one concrete operating point in a boxed readout** — real numbers at a specific point, not generic axis labels; this is the "so what" turned into a screenshot-able stat.
6. **Animate by sweeping the operating point across the domain** — usually a load/angle parameter rather than time, with curves static and only the marker/readout moving.

**Divergences from this project's pattern:** his theme is light, not dark-branded (stylistic choice only); his panels rarely share one physical clock, so the "sweep" is often an operating condition, not `t`; his annotation density is much higher, with boxed callouts carrying narrative weight this project currently puts mostly in the footer.
