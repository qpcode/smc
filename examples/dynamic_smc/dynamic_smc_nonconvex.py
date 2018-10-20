
import random
import matplotlib.pyplot as plt
from matplotlib import patches
import os

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.dynamic_smc import DynamicSMC


if __name__ == '__main__':


    # Define probability distribution
    xmin, xmax = (-100.0, 100.0)
    ymin, ymax = (-100.0, 100.0)
    prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=100, Ny=100)

    # first set everything to zero
    prob_dist.set_zero()

    # set distribution on ring and square
    prob_dist.set_value_in_circle(0.0, 0.0, 75.0, 1.0)
    prob_dist.set_value_in_circle(0.0, 0.0, 60, 0.0)
    prob_dist.set_value_in_rect(-20, 20, -20, 20, 1.0)

    # Define DynamicSMC object
    dynamic_smc = DynamicSMC(prob_dist)
    n_agents = 25
    random.seed(1434)
    # add agents to coverage object
    for _ in range(n_agents):
        random_state = (xmin + (xmax - xmin) * random.random(),
                        ymin + (ymax - ymin) * random.random())
        dynamic_smc.add_agent(Agent(random_state[0], random_state[1]))

    animation_folder = 'dynamic_smc_nonconvex'
    if not os.path.exists(animation_folder):
        os.makedirs(animation_folder)

    # defining colors for each agents for plotting
    colors = [[random.random() for _ in range(3)] for _ in range(n_agents)]

    plt.figure(figsize=(10, 10))
    # plot the domain
    outer_circle = patches.Ellipse((0.0, 0.0), 2 * 75.0, 2 * 75.0, linewidth=1, facecolor='b', alpha=0.2)
    inner_circle = patches.Ellipse((0.0, 0.0), 2 * 60.0, 2 * 60.0, linewidth=1, facecolor='w', edgecolor='w', alpha=1.0)
    square = patches.Rectangle((-20.0, -20.0), 40.0, 40.0, linewidth=1, facecolor='b', alpha=0.2)
    ax = plt.gca()
    ax.add_patch(outer_circle)
    ax.add_patch(inner_circle)
    ax.add_patch(square)

    # Run the algorithm (1000 time-steps of size 1.0)
    for anim_ind in range(1000):
        print 'Running Step', anim_ind, 'of animation.'
        dynamic_smc.time_steps(1, 1.0)

        # plotting current location of agents
        for ind, agent in enumerate(dynamic_smc.agents):
            plt.plot(agent.x, agent.y, '.', color=colors[ind], markersize=3)

        plt.axis('equal')
        plt.axis([xmin, xmax, ymin, ymax])
        ax = plt.gca()
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_adjustable('box')
        out_fig_name = os.path.join(animation_folder,
                                    'dynamic_smc_nonconvex_%03d.jpg' % anim_ind)

        if anim_ind % 10 == 0:
            plt.savefig(out_fig_name, bbox_inches='tight')
