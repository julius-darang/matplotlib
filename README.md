# EE & Math Visualisation Series — code.arts

Animated and static visual explanations of fundamental electrical engineering concepts using matplotlib. Each topic follows a two-panel "Hero + Side" layout with a consistent dark theme.

## Topics

| Topic | File | Output |
|---|---|---|
| **Ohm's Law** — I vs R (hyperbola) and I vs V (line) | `scripts/ohms_law.py` | PNG + GIF |
| **RC Time Constant** — capacitor charge/discharge | `scripts/capacitor_rc.py` | GIF |
| **RL Time Constant** — inductor buildup/decay | `scripts/inductor_rl.py` | GIF |
| **Resonant Frequency** — f₀ sensitivity to C | `scripts/resonant_frequency.py` | GIF |
| **Series vs Parallel** — equivalent resistance | `scripts/series_parallel.py` | PNG |
| **Short Circuit** — fault current vs distance | `scripts/short_circuit.py` | PNG |
| **Voltage Divider** — Vout swept across R₂ range | `scripts/voltage_divider.py` | GIF |

## Structure

```
├── physics/          # Pure computation, one module per topic
├── scripts/          # matplotlib figures and animations
├── theme.py          # Dark palette, header/footer helpers
├── animate.py        # FuncAnimation wrapper + GIF export
└── outputs/          # Generated PNGs and GIFs
```

## Requirements

- Python ≥ 3.9
- `matplotlib`
- `numpy`

```sh
pip install matplotlib numpy
```

## Usage

```sh
python scripts/ohms_law.py
```

Outputs appear in `outputs/`. To edit parameters, modify the constants at the top of each script.

## Design

- **`physics/`** — pure functions (no plotting) for each circuit law.
- **`scripts/`** — imports from `physics`, builds matplotlib figures, exports PNG/GIF.
- **`theme.py`** — dark background, orange accent, DM Mono / Inter fonts. Call `theme.apply()` once per script.
- **`animate.py`** — wraps `matplotlib.animation.FuncAnimation`; pass a figure, an update callback, and a frame count.

## Credits

Created by [code.arts](https://x.com/code_arts_).
