import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def make_animation(fig, update_fn, n_frames, fps=20):
    anim = animation.FuncAnimation(
        fig, update_fn, frames=n_frames, blit=False, interval=1000 / fps
    )
    return anim


def save_gif(anim, path, fps=20):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    anim.save(path, writer=animation.PillowWriter(fps=fps))
    print(f"saved {path}")