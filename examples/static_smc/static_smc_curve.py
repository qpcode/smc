

import random
import matplotlib.pyplot as plt
from math import sin, cos, pi
import numpy as np

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.static_smc import StaticSMC


def hypocycloid_curve(theta, r=0.2, k=5):
    """ defines parametric curve for hypocycloid curve """

    x = r * (k-1) * cos(theta) + r * cos((k-1) * theta)
    y = r * (k-1) * sin(theta) - r * sin((k-1) * theta)

    return x, y


if __name__ == '__main__':

    # Define probability distribution
    xmin, xmax = (-1.0, 1.0)
    ymin, ymax = (-1.0, 1.0)
    prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
    prob_dist.set_prob_dist_on_curve(hypocycloid_curve,
                                     np.arange(0, 2*pi, 0.01))

    # Define StaticSMC coverage object
    static_smc = StaticSMC(prob_dist)
    n_agents = 50
    random.seed(100418)
    initial_states = []
    # add agents to coverage object
    for iagent in range(n_agents):
        random_state = (xmin + (xmax-xmin) * random.random(),
                        ymin + (ymax-ymin) * random.random())
        static_smc.add_agent(Agent(random_state[0], random_state[1]))
        initial_states.append(random_state)

    # Run the algorithm (100 time-steps of size 0.01)
    static_smc.time_steps(100, 0.01)

    final_states = []
    for agent in static_smc.agents:
        final_states.append((agent.x, agent.y))

    points_on_curve = [hypocycloid_curve(th) for th in np.arange(0, 2*pi, 0.01)]
    xs_on_curve = [x[0] for x in points_on_curve]
    ys_on_curve = [x[1] for x in points_on_curve]

    plt.figure(figsize=(14, 6))
    # plotting initial locations of each agent
    plt.subplot(1, 2, 1)
    for state in initial_states:
        plt.plot(state[0], state[1], 'o', markersize=8)
    plt.plot(xs_on_curve, ys_on_curve, 'k-')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title('Initial states')

    # plotting final configuration of agents
    plt.subplot(1, 2, 2)
    for state in final_states:
        plt.plot(state[0], state[1], 'o', markersize=8)
        plt.plot(xs_on_curve, ys_on_curve, 'k-')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title('Final Static SMC configuration')
    plt.show()

