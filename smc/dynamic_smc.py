""" Defines class for Dynamic SMC """

import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, pi, pow
from itertools import product

from probdist import ProbDist
from coverage import Coverage
from agent import Agent, AgentTrajectories


class DynamicSMC(Coverage):
    """ Class for Dynamic Coverage problems """
    def __init__(self, target_distribution):
        """ Constructor for DynamicSMC class """
        super(DynamicSMC, self).__init__(target_distribution)

        Nx = self.target_distribution.Nx
        Ny = self.target_distribution.Ny

        self.current_time = 0
        self.C_k = np.zeros((Nx, Ny))

    def _update_C_k(self, dt):
        """ Updates Fourier coefficients of Coverage distribution """

        Nx = self.target_distribution.Nx
        Ny = self.target_distribution.Ny

        Lx = self.target_distribution.xmax - self.target_distribution.xmin
        Ly = self.target_distribution.ymax - self.target_distribution.ymin
        xmin = self.target_distribution.xmin
        ymin = self.target_distribution.ymin

        for agent in self.agents:
            (xpos, ypos) = (agent.x, agent.y)
            (xrel, yrel) = (xpos - xmin, ypos - ymin)
            for kx, ky in product(range(Nx), range(Ny)):
                self.C_k[kx, ky] += cos(kx * pi * xrel/Lx) * cos(ky * pi * yrel/Ly) * dt

        return

    def time_steps(self, n_steps, dt, return_trajectories=False):
        """ Executes given number of steps of SMC algorithm with time-step dt """

        # First compute mu_k of target distribution
        self.target_distribution.compute_mu_k()

        mu_k = self.target_distribution.get_mu_k()

        n_agents = len(self.agents)

        if return_trajectories:
            trajectories = []
            for iagent, agent in enumerate(self.agents):
                new_trajectory = AgentTrajectories()
                new_trajectory.add_point(agent.x, agent.y)
                trajectories.append(new_trajectory)

        for i_step in range(n_steps):
            self._update_C_k(dt)
            self.current_time += 1
            S_k = self.C_k - mu_k * n_agents * self.current_time * dt

            for iagent, agent in enumerate(self.agents):

                Bjx, Bjy = self.compute_Bjvec_from_Sk(S_k, agent)

                Bjnorm = np.sqrt(Bjx * Bjx + Bjy * Bjy)

                (agent.x, agent.y) = (agent.x - (Bjx / Bjnorm) * dt,
                                      agent.y - (Bjy / Bjnorm) * dt)

                self.reflect_agent(agent)

                if return_trajectories:
                    trajectories[iagent].add_point(agent.x, agent.y)

            print '\r Finished %d / %d steps of DynamicSMC' % (i_step + 1, n_steps),

        print '\nDone.'

        if return_trajectories:
            return trajectories
        else:
            return

