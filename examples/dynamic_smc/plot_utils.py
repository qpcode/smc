
import matplotlib.pyplot as plt
import numpy as np


def plot_density(prob_dist):
    """" plots the given density """

    xmin = prob_dist.xmin
    xmax = prob_dist.xmax
    ymin = prob_dist.xmin
    ymax = prob_dist.xmax
    dx = prob_dist.dx
    dy = prob_dist.dy

    y, x = np.mgrid[slice(ymin, ymax+dy, dy),
                    slice(xmin, xmax+dx, dx)]

    ax = plt.gca()
    ax.pcolormesh(x, y, prob_dist.mu.T, cmap='Greens')

    return


def plot_trajectories(trajectories, colors, plot_end=True):
    """ plots a list of given trajectories """

    for traj, col in zip(trajectories, colors):
        plt.plot(traj.xs, traj.ys, color=col)
        if plot_end:
            plt.plot(traj.xs[-1], traj.ys[-1], 'o', color=col)

    return
