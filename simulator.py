import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap

def simulate_correlated_walk(n_steps=20000,
                             step_length=1.0,
                             kappa=50.0,
                             bounds=(100, 100),
                             seed=None):
    """
    Correlated random walk using von Mises for turning angle.
    """
    rng = np.random.default_rng(seed)
    xmax, ymax = bounds
    xmin, ymin = 0, 0

    pos = np.zeros((n_steps, 2))
    theta = rng.uniform(0, 2*np.pi)  # initial heading

    x, y = (xmax - xmin) * 0.5, (ymax - ymin) * 0.5
    pos[0] = [x, y]

    for i in range(1, n_steps):

        # Turn angle from von Mises distribution
        dtheta = rng.vonmises(mu=0.0, kappa=kappa)
        theta = theta + dtheta
        
        # Step forward
        dx = step_length * np.cos(theta)
        dy = step_length * np.sin(theta)
        x = x + dx
        y = y + dy

        # Reflective boundaries
        if x <= xmin:
            x = xmin + (xmin - x)
            theta = np.pi - theta
        if x >= xmax:
            x = xmax - (x - xmax)
            theta = np.pi - theta
        if y <= ymin:
            y = ymin + (ymin - y)
            theta = -theta
        if y >= ymax:
            y = ymax - (y - ymax)
            theta = -theta

        # Store position
        pos[i] = [x, y]

    return pos

# Main execution
if __name__ == "__main__":

    # Simuation Parameters
    params = {
        "n_steps": 1000000,    # number of steps
        "step_length": 0.3,    # length of each step
        "kappa": 50.0,         # concentration parameter for von Mises
        "bounds": (1600, 900), # (width, height) of the area
        "seed": 42             # random seed for reproducibility
    }

    # Call the simulation function
    pos = simulate_correlated_walk(**params)

    # Plotting
    segments = np.concatenate([pos[:-1, None, :], pos[1:, None, :]], axis=1)

    # Create the custom colormap
    base_colors = ["#000000", "#bb0000"]
    my_cmap = LinearSegmentedColormap.from_list("my_cmap", base_colors, N=256)
    t = np.linspace(0, 1, len(segments))  # normalized time 0–1
    colors = my_cmap(t)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Create and Add LineCollection
    lc = LineCollection(segments, colors=colors, linewidth=0.7, capstyle='round')
    ax.add_collection(lc)

    # Set limits and aspect
    ax.set_xlim(pos[:, 0].min(), pos[:, 0].max())
    ax.set_ylim(pos[:, 1].min(), pos[:, 1].max())
    ax.set_aspect('equal')
    ax.axis('off')

    # Show plot
    plt.tight_layout()
    plt.show()