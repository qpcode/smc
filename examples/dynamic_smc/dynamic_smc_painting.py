
import random
import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np
import os

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.dynamic_smc import DynamicSMC


def update_paint_dens(paint_dens, prob_dist, x_curr, y_curr, paint_rate):
    """ Updates paint density array based on current location of agents """
    for x, y in zip(x_curr, y_curr):

        ix = int((x - prob_dist.xmin) / prob_dist.dx)
        iy = int((y - prob_dist.ymin) / prob_dist.dy)

        paint_dens[ix, iy] += paint_rate

    return paint_dens

if __name__ == '__main__':

    # read image
    image = imread('lady_painting.jpg')

    image_dens = 255.0 - image.T
    image_dens = np.fliplr(image_dens)

    n_agents = 20
    n_time_steps = 10000
    paint_rate = sum(sum(image_dens)) / float(n_time_steps * n_agents)

    # initializing paint density array
    paint_dens = np.zeros(image_dens.shape)

    # Define probability distribution
    xmin, ymin = (0, 0)
    xmax, ymax = image_dens.shape
    prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=xmax, Ny=ymax)
    prob_dist.set_prob_dist_from_array(image_dens)

    # Define DynamicSMC object
    dynamic_smc = DynamicSMC(prob_dist)

    # add agents to coverage object
    for _ in range(n_agents):
        dynamic_smc.add_agent(Agent(xmin + random.random() * (xmax-xmin),
                                    ymin + random.random() * (ymax-ymin)))

    animation_folder = 'dynamic_smc_painting'
    if not os.path.exists(animation_folder):
        os.makedirs(animation_folder)

    # Run the algorithm (10000 time-steps)
    for time_ind in range(n_time_steps):
        print 'Running Step', time_ind, 'of animation.'

        dynamic_smc.time_steps(1, 1.0)

        # plot current location of agent
        x_curr = []
        y_curr = []
        for agent in dynamic_smc.agents:
            x_curr.append(agent.x)
            y_curr.append(agent.y)

        paint_dens = update_paint_dens(paint_dens, prob_dist, x_curr, y_curr, paint_rate)

        if time_ind % 20 == 0:

            plt.imshow(255.0 - np.fliplr(paint_dens).T, cmap='gray', vmin=0, vmax=255.0)
            plt.axis('equal')
            ax = plt.gca()
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_adjustable('box')

            out_fig_name = os.path.join(animation_folder,
                                       'dynamic_smc_painting_%05d.jpg' % time_ind)

            plt.savefig(out_fig_name, bbox_inches='tight')
            plt.close()