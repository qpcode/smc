
import random
import matplotlib.pyplot as plt

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.dynamic_smc import DynamicSMC

import plot_utils


if __name__ == '__main__':


    # Define probability distribution
    prob_dist = ProbDist(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0)
    # Define DynamicSMC object
    dynamic_smc = DynamicSMC(prob_dist)
    n_agents = 4
    random.seed(967218)
    # add agents to coverage object
    for iagent in range(n_agents):
        dynamic_smc.add_agent(Agent(random.random(), random.random()))

    # defining colors for each agents for plotting
    colors = [[random.random() for _ in range(3)] for _ in range(n_agents)]

    print 'First run:'
    # First run the algorithm for 500 time-steps
    first_run_trajectories = dynamic_smc.time_steps(500, 0.01, return_trajectories=True)

    # plot trajectories
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plot_utils.plot_trajectories(first_run_trajectories, colors)
    plt.axis([0, 1, 0, 1])
    plt.title('Trajectories after 500 time-steps')

    print 'Second run:'
    # run the algorithm for 500 more time-steps
    second_run_trajectories = dynamic_smc.time_steps(500, 0.01, return_trajectories=True)
    plt.subplot(1, 2, 2)
    plot_utils.plot_trajectories(first_run_trajectories, colors, plot_end=False)
    plot_utils.plot_trajectories(second_run_trajectories, colors)
    plt.axis([0, 1, 0, 1])
    plt.title('Trajectories after 1000 time-steps')
    plt.show()
