

import random
import matplotlib.pyplot as plt
from matplotlib import patches

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.static_smc import StaticSMC

if __name__ == '__main__':

    # Define probability distribution
    prob_dist = ProbDist(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0)
    prob_dist.set_value_in_rect(0.2, 0.5, 0.7, 0.8, 0.0)
    prob_dist.set_value_in_ellipse(0.7, 0.3, 0.15, 0.05, 0.0)
    # Define StaticSMC coverage object
    static_smc = StaticSMC(prob_dist)
    n_agents = 1000
    random.seed(83318)
    initial_states = []
    # add agents to coverage object
    for iagent in range(n_agents):
        random_state = (random.random(), random.random())
        static_smc.add_agent(Agent(random_state[0], random_state[1]))
        initial_states.append(random_state)

    # Run the algorithm (100 time-steps of size 0.001)
    static_smc.time_steps(100, 0.001)

    final_states = []
    for agent in static_smc.agents:
        final_states.append((agent.x, agent.y))

    plt.figure(figsize=(14, 6))
    # plotting initial locations of each agent
    plt.subplot(1, 2, 1)
    rect = patches.Rectangle((0.2, 0.7), 0.3, 0.1, linewidth=1, facecolor='b', alpha=0.5)
    ellipse = patches.Ellipse((0.7, 0.3), 0.3, 0.1, linewidth=1, facecolor='r', alpha=0.5)
    ax = plt.gca()
    ax.add_patch(rect)
    ax.add_patch(ellipse)
    for state in initial_states:
        plt.plot(state[0], state[1], 'o', markersize=3)
    plt.axis([0, 1, 0, 1])
    plt.title('Initial states')

    # plotting final configuration of agents
    plt.subplot(1, 2, 2)
    rect = patches.Rectangle((0.2, 0.7), 0.3, 0.1, linewidth=1, facecolor='b', alpha=0.5)
    ellipse = patches.Ellipse((0.7, 0.3), 0.3, 0.1, linewidth=1, facecolor='r', alpha=0.5)
    ax = plt.gca()
    ax.add_patch(rect)
    ax.add_patch(ellipse)
    for state in final_states:
        plt.plot(state[0], state[1], 'o', markersize=3)
    plt.axis([0, 1, 0, 1])
    plt.title('Final Static SMC configuration')
    plt.show()

