

import random
import matplotlib.pyplot as plt
import numpy as np

from smc.probdist import ProbDist
from smc.agent import Agent
from smc.static_smc import StaticSMC


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


if __name__ == '__main__':

    # Define probability distribution
    xmin, xmax = (-100.0, 100.0)
    ymin, ymax = (-100.0, 100.0)
    prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=100, Ny=100)
    # first set everything to zero
    prob_dist.set_zero()
    # mean of gaussian distribution
    mu_x, mu_y = (35, 25)
    mu = np.array([[mu_x], [mu_y]])
    # covariance of gaussian distribution
    sig_x, sig_y = (35, 40)
    cov = np.array([[sig_x*sig_x, 0], [0, sig_y*sig_y]])
    # adding gaussian distribution
    prob_dist.add_gaussian(mu, cov, 1.0)

    # Define StaticSMC coverage object
    static_smc = StaticSMC(prob_dist)
    n_agents = 200
    random.seed(100818)
    initial_states = []
    # add agents to coverage object
    for iagent in range(n_agents):
        random_state = (xmin + (xmax-xmin) * random.random(),
                        ymin + (ymax-ymin) * random.random())
        static_smc.add_agent(Agent(random_state[0], random_state[1]))
        initial_states.append(random_state)

    # Run the algorithm (200 time-steps of size 1)
    static_smc.time_steps(200, 1)

    final_states = []
    for agent in static_smc.agents:
        final_states.append((agent.x, agent.y))

    plt.figure(figsize=(14, 6))
    # plotting initial locations of each agent
    plt.subplot(1, 2, 1)
    plot_density(prob_dist)
    for state in initial_states:
        plt.plot(state[0], state[1], 'ro')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title('Initial states')

    # plotting final configuration of agents
    plt.subplot(1, 2, 2)
    plot_density(prob_dist)
    for state in final_states:
        plt.plot(state[0], state[1], 'ro')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title('Final Static SMC configuration')
    plt.show()

