

import random
import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np
import os

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.static_smc import StaticSMC

if __name__ == '__main__':

    # read image
    image = imread('heisenberg.jpg')

    image_dens = 255.0 - image.T
    image_dens = np.fliplr(image_dens)

    # Define probability distribution
    xmin, ymin = (0, 0)
    xmax, ymax = image_dens.shape
    prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=xmax, Ny=ymax)
    prob_dist.set_prob_dist_from_array(image_dens)

    # Define StaticSMC coverage object
    static_smc = StaticSMC(prob_dist)
    n_agents = 2000
    random.seed(100118)

    # add agents to coverage object
    for _ in range(n_agents):
        random_state = (random.random() * xmax, random.random() * ymax)
        static_smc.add_agent(Agent(random_state[0], random_state[1]))

    animation_folder = 'heisenberg_animation'
    if not os.path.exists(animation_folder):
        os.makedirs(animation_folder)

    # Run the algorithm (150 time-steps of size 0.125)
    for anim_ind in range(150):
        print 'Running Step', anim_ind, 'of animation.'
        static_smc.time_steps(1, 0.125)

        current_states = []
        for agent in static_smc.agents:
            current_states.append((agent.x, agent.y))

        # plotting current location of agents
        plt.figure(figsize=(4, 6))
        for state in current_states:
            plt.plot(state[0], state[1], 'k.', markersize=2)
        plt.axis('equal')
        plt.axis([0-20, xmax+20, 0-20, ymax+20])
        plt.text(xmin + 10, ymax+10, 'SAY MY NAME')
        ax = plt.gca()
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_adjustable('box')
        out_fig_name = os.path.join(animation_folder,
                                    'heisenberg_%03d.jpg' % anim_ind)
        plt.savefig(out_fig_name, bbox_inches='tight')
        plt.close()

    # Now use your favorite image processing tool to
    # stitch these images to form a GIF animation

