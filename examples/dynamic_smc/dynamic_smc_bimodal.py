
import random
import numpy as np
import matplotlib.pyplot as plt
import os

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.dynamic_smc import DynamicSMC

import plot_utils


if __name__ == '__main__':


    # Define probability distribution
    xmin, xmax = (-100.0, 100.0)
    ymin, ymax = (-100.0, 100.0)
    prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=100, Ny=100)
    # first set everything to zero
    prob_dist.set_zero()

    # adding first gaussian
    # mean of gaussian distribution
    mu_x, mu_y = (35, 25)
    mu = np.array([[mu_x], [mu_y]])
    # covariance of gaussian distribution
    sig_x, sig_y = (35, 40)
    cov = np.array([[sig_x * sig_x, 0], [0, sig_y * sig_y]])
    prob_dist.add_gaussian(mu, cov, 1.0)

    # adding second gaussian
    # mean of gaussian distribution
    mu_x, mu_y = (-50, -45)
    mu = np.array([[mu_x], [mu_y]])
    # covariance of gaussian distribution
    sig_x, sig_y = (40, 35)
    cov = np.array([[sig_x * sig_x, 0], [0, sig_y * sig_y]])
    prob_dist.add_gaussian(mu, cov, 1.0)

    # Define DynamicSMC object
    dynamic_smc = DynamicSMC(prob_dist)
    n_agents = 10
    random.seed(967218)
    # add agents to coverage object
    for _ in range(n_agents):
        random_state = (xmin + (xmax - xmin) * random.random(),
                        ymin + (ymax - ymin) * random.random())
        dynamic_smc.add_agent(Agent(random_state[0], random_state[1]))

    animation_folder = 'dynamic_smc_bimodal'
    if not os.path.exists(animation_folder):
        os.makedirs(animation_folder)

    # defining colors for each agents for plotting
    colors = [[random.random() for _ in range(3)] for _ in range(n_agents)]

    plt.figure(figsize=(10, 10))
    plot_utils.plot_density(prob_dist)

    # Run the algorithm (1000 time-steps of size 1.0)
    for anim_ind in range(1000):
        print 'Running Step', anim_ind, 'of animation.'
        dynamic_smc.time_steps(1, 1.0)

        current_states = []
        for agent in dynamic_smc.agents:
            current_states.append((agent.x, agent.y))

        # plotting current location of agents
        for ind, state in enumerate(current_states):
            plt.plot(state[0], state[1], '.', color=colors[ind], markersize=3)

        plt.axis('equal')
        plt.axis([xmin, xmax, ymin, ymax])
        ax = plt.gca()
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_adjustable('box')
        out_fig_name = os.path.join(animation_folder,
                                    'dynamic_smc_bimodal_%03d.jpg' % anim_ind)

        if anim_ind % 10 == 0:
            plt.savefig(out_fig_name, bbox_inches='tight')
