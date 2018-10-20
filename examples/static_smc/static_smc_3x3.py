

import random
import matplotlib.pyplot as plt

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.static_smc import StaticSMC

if __name__ == '__main__':

    # Define probability distribution
    prob_dist = ProbDist(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0)
    # Define StaticSMC coverage object
    static_smc = StaticSMC(prob_dist)
    n_agents = 9
    random.seed(100118)
    initial_states = []
    # add agents to coverage object
    for iagent in range(n_agents):
        random_state = (random.random(), random.random())
        static_smc.add_agent(Agent(random_state[0], random_state[1]))
        initial_states.append(random_state)

    # Run the algorithm (2000 time-steps of size 0.01)
    static_smc.time_steps(2000, 0.01)

    final_states = []
    for agent in static_smc.agents:
        final_states.append((agent.x, agent.y))

    plt.figure(figsize=(14, 6))
    # plotting initial locations of each agent
    plt.subplot(1, 2, 1)
    for state in initial_states:
        plt.plot(state[0], state[1], 'o')
    plt.axis([0, 1, 0, 1])
    plt.title('Initial states')
    # plotting final configuration of agents
    plt.subplot(1, 2, 2)
    for state in final_states:
        plt.plot(state[0], state[1], 'o')
    plt.axis([0, 1, 0, 1])
    plt.title('Final Static SMC configuration')
    plt.show()

