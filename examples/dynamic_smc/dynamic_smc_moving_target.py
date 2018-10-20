
import random
import matplotlib.pyplot as plt
from matplotlib import patches
import os

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.dynamic_smc import DynamicSMC


if __name__ == '__main__':


    # Define probability distribution
    prob_dist = ProbDist()

    # Define DynamicSMC object
    dynamic_smc = DynamicSMC(prob_dist)
    random.seed(101418)

    # add one agent to coverage object
    dynamic_smc.add_agent(Agent(0.1, 0.1))

    animation_folder = 'dynamic_smc_moving_target'
    if not os.path.exists(animation_folder):
        os.makedirs(animation_folder)

    plt.figure(figsize=(10, 10))

    agent = dynamic_smc.agents[0]
    x_prev, y_prev = (agent.x, agent.y)

    # Run the algorithm (1000 time-steps)
    for time_ind in range(1000):
        print 'Running Step', time_ind, 'of animation.'

        center1 = (0.2 + time_ind * 6e-4, 0.2)
        center2 = (0.2 + time_ind * 6e-4, 0.8)
        circle_radius = 0.1

        prob_dist.set_zero()
        prob_dist.set_value_in_circle(center1[0], center1[1], circle_radius, 1.0)
        prob_dist.set_value_in_circle(center2[0], center2[1], circle_radius, 1.0)

        dynamic_smc.time_steps(1, 0.02)

        # plot moving target distribution
        ax = plt.gca()
        circle1 = patches.Ellipse(center1, 2 * circle_radius, 2 * circle_radius, linewidth=1, facecolor='r', alpha=0.2)
        circle2 = patches.Ellipse(center2, 2 * circle_radius, 2 * circle_radius, linewidth=1, facecolor='r', alpha=0.2)
        ax.add_patch(circle1)
        ax.add_patch(circle2)

        # plot current location of agent
        agent = dynamic_smc.agents[0]
        x_curr, y_curr = (agent.x, agent.y)
        plt.plot([x_prev, x_curr], [y_prev, y_curr], '-', color='b', markersize=4)
        agent_pos = patches.Ellipse((x_curr, y_curr), 0.01, 0.01, facecolor='b', alpha=0.5)
        ax.add_patch(agent_pos)
        x_prev, y_prev = (x_curr, y_curr)

        plt.axis('equal')
        plt.axis([0, 1, 0, 1])
        ax = plt.gca()
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.set_adjustable('box')
        out_fig_name = os.path.join(animation_folder,
                                    'dynamic_smc_moving_target_%03d.jpg' % time_ind)

        if time_ind % 2 == 0:
            plt.savefig(out_fig_name, bbox_inches='tight')

        circle1.remove()
        circle2.remove()
        agent_pos.remove()
