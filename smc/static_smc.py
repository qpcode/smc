""" Defines class for Static SMC """

import numpy as np
from math import cos, pi
from itertools import product

from coverage import Coverage


class StaticSMC(Coverage):
    """ Class for Static Coverage problems """
    def __init__(self, target_distribution):
        """ Constructor for StaticSMC class """
        super(StaticSMC, self).__init__(target_distribution)

    def _get_c_k(self):
        """ Returns Fourier coefficients of Coverage distribution """

        Nx = self.target_distribution.Nx
        Ny = self.target_distribution.Ny

        c_k = np.zeros((Nx, Ny))

        n_agents = len(self.agents)

        Lx = self.target_distribution.xmax - self.target_distribution.xmin
        Ly = self.target_distribution.ymax - self.target_distribution.ymin
        xmin = self.target_distribution.xmin
        ymin = self.target_distribution.ymin

        for agent in self.agents:
            (xpos, ypos) = (agent.x, agent.y)
            (xrel, yrel) = (xpos - xmin, ypos - ymin)
            for kx, ky in product(range(Nx), range(Ny)):
                c_k[kx, ky] += cos(kx * pi * xrel/Lx) * cos(ky * pi * yrel/Ly)

        c_k = c_k / n_agents

        return c_k

    def time_steps(self, n_steps, dt):
        """ Generates trajectories for the agents to be deployed to a
        Static SMC configuration """

        # First compute mu_k of target distribution
        self.target_distribution.compute_mu_k()

        mu_k = self.target_distribution.get_mu_k()

        for i_step in range(n_steps):
            c_k = self._get_c_k()
            s_k = c_k - mu_k

            for agent in self.agents:

                Bjx, Bjy = self.compute_Bjvec_from_Sk(s_k, agent)

                Bjnorm = np.sqrt(Bjx * Bjx + Bjy * Bjy)

                (agent.x, agent.y) = (agent.x - (Bjx / Bjnorm) * dt,
                                      agent.y - (Bjy / Bjnorm) * dt)

                self.reflect_agent(agent)

            print '\r Finished %d / %d steps of StaticSMC' % (i_step + 1, n_steps),

        print '\nDone.'

        return

