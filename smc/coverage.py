""" Defines abstract class for coverage problems """

import matplotlib.pyplot as plt
from math import sin, cos, pi, pow
from itertools import product

class Coverage(object):
	""" Abstract class for coverage problems """
	def __init__(self, target_distribution):
		""" Constructor for Coverage class """
		self.target_distribution = target_distribution
		self.agents = []

	def add_agent(self, new_agent):
		""" Adds new agent to the coverage problem """
		self.agents.append(new_agent)

	def reflect_agent(self, agent):
		""" Makes sure that agent location is within bounds of target distribution """
		xmin = self.target_distribution.xmin
		ymin = self.target_distribution.ymin
		xmax = self.target_distribution.xmax
		ymax = self.target_distribution.ymax

		if agent.x < xmin:
			agent.x = xmin + (xmin - agent.x)
		if agent.x > xmax:
			agent.x = xmax - (agent.x - xmax)

		if agent.y < ymin:
			agent.y = ymin + (ymin - agent.y)
		if agent.y > ymax:
			agent.y = ymax - (agent.y - ymax)

	def compute_Bjvec_from_Sk(self, S_k, agent):
		""" Computes the vector Bj for given agent and S_k (difference between
		target distribution and coverage distribution Fourier coefficients)
		 """

		Nx = S_k.shape[0]
		Ny = S_k.shape[1]

		Lx = self.target_distribution.xmax - self.target_distribution.xmin
		Ly = self.target_distribution.ymax - self.target_distribution.ymin
		xmin = self.target_distribution.xmin
		ymin = self.target_distribution.ymin

		(xpos, ypos) = (agent.x, agent.y)
		(xrel, yrel) = (xpos - xmin, ypos - ymin)
		Bjx = 0.0
		Bjy = 0.0
		for kx, ky in product(range(Nx), range(Ny)):
			lambda_k = 1.0 / pow(1.0 + kx * kx + ky * ky, 1.5)
			fkip = 1.0
			if kx != 0:
				fkip *= 0.5
			if ky != 0:
				fkip *= 0.5

			Bjx += (lambda_k / fkip) * S_k[kx, ky] * (-kx * pi / Lx) * \
				   sin(kx * pi * xrel / Lx) * cos(ky * pi * yrel / Ly)

			Bjy += (lambda_k / fkip) * S_k[kx, ky] * (-ky * pi / Ly) * \
				   cos(kx * pi * xrel / Lx) * sin(ky * pi * yrel / Ly)

		return Bjx, Bjy


	def plot_agents(self):
		""" Plots the current location of agents """

		xmin = self.target_distribution.xmin
		ymin = self.target_distribution.ymin
		xmax = self.target_distribution.xmax
		ymax = self.target_distribution.ymax

		# first print out agent locations
		print 'Current Agent locations'
		for agent in self.agents:
			print agent.x, agent.y

		for agent in self.agents:
			plt.plot(agent.x, agent.y, 'ro')
		plt.axis([xmin, xmax, ymin, ymax])
		plt.show()
