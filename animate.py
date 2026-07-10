"""
animate.py
Generic FuncAnimation wrapper. Every topic (out-of-step, fault
clearing time, voltage recovery, etc.) plugs in a single "sweep
parameter" + an update(frame) callback that redraws each panel from
values already computed by physics.py — mirroring how the delta sweep
in the reference GIF drove all three panels from one loop variable.
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def make_animation(fig, update_fn, n_frames, fps=20):
    """
    update_fn(frame_index) -> None
        Mutates existing artists (line.set_data, scatter.set_offsets,
        etc.) in place. Don't call ax.plot()/ax.clear() every frame —
        that's what makes GIFs slow and re-renders text sloppily.
    """
    anim = animation.FuncAnimation(
        fig, update_fn, frames=n_frames, blit=False, interval=1000 / fps
    )
    return anim


def save_gif(anim, path, fps=20):
    anim.save(path, writer=animation.PillowWriter(fps=fps))
    print(f"saved {path}")