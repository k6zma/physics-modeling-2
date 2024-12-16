import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tempfile
import numpy as np
import streamlit as st
from stqdm import stqdm


def animate_trajectory(x, y, total_frames=200, fps=24):
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor("none")

    ax.set_facecolor("none")

    ax.plot(x, y, label="y(x)")
    ax.set_xlabel("X (м)")
    ax.set_ylabel("Y (м)")

    ax.set_title("Траектория движения электрона")

    ax.grid(True)
    ax.legend()

    (particle,) = ax.plot([], [], "ro", markersize=6)

    frames = min(total_frames, len(x))
    x_uniform = np.interp(np.linspace(0, 1, frames), np.linspace(0, 1, len(x)), x)
    y_uniform = np.interp(np.linspace(0, 1, frames), np.linspace(0, 1, len(y)), y)

    def init():
        particle.set_data([], [])
        return (particle,)

    def update(frame):
        particle.set_data([x_uniform[frame]], [y_uniform[frame]])
        return (particle,)

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as temp_file:
        writer = animation.PillowWriter(fps=fps)

        with stqdm(total=frames) as pbar:
            ani = animation.FuncAnimation(
                fig,
                update,
                frames=frames,
                init_func=init,
                blit=True,
                repeat=False,
            )

            ani.save(
                temp_file.name,
                writer=writer,
                progress_callback=lambda i, n: pbar.update(1),
            )

        temp_file.seek(0)
        gif_data = temp_file.read()

    st.image(gif_data)
