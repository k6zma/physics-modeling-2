import matplotlib.pyplot as plt


def plot_graphs(t, x, y, vy, ay):
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    axs[0, 0].plot(x, y)
    axs[0, 0].set_title("y(x)")
    axs[0, 0].set_xlabel("x (м)")
    axs[0, 0].set_ylabel("y (м)")
    axs[0, 0].grid(True)

    axs[0, 1].plot(t, vy)
    axs[0, 1].set_title("Vy(t)")
    axs[0, 1].set_xlabel("t (с)")
    axs[0, 1].set_ylabel("Vy (м/с)")
    axs[0, 1].grid(True)

    axs[1, 0].plot(t, ay)
    axs[1, 0].set_title("ay(t)")
    axs[1, 0].set_xlabel("t (с)")
    axs[1, 0].set_ylabel("ay (м/с^2)")
    axs[1, 0].grid(True)

    axs[1, 1].plot(t, y)
    axs[1, 1].set_title("y(t)")
    axs[1, 1].set_xlabel("t (с)")
    axs[1, 1].set_ylabel("y (м)")
    axs[1, 1].grid(True)

    fig.tight_layout()

    return fig
