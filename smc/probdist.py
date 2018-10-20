""" Defines a class for capturing Probability Distributions """

import numpy as np
from scipy.fftpack import dct
from itertools import product
from math import cos, pi
from functools import partial


class ProbDist:
    """ Class for Probability Distributions """
    def __init__(self, xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0, Nx=50, Ny=50):
        """ Constructor for ProbDist class """
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.Nx = Nx
        self.Ny = Ny
        self.dx = float(self.xmax - self.xmin) / float(self.Nx)
        self.dy = float(self.ymax - self.ymin) / float(self.Ny)
        # numpy array for target probability distribution
        self.mu = np.ones((self.Nx, self.Ny))
        # numpy array for fourier coefficients of target probability distribution
        self.mu_k = np.zeros((self.Nx, self.Ny))
        # boolean that indicates whether fourier coefficients of
        # target probability distribution are current
        self.mu_k_current = False

    def get_mu_k(self):
        """ Returns Fourier coefficients of probability distribution """
        return self.mu_k

    def normalize_mu(self):
        """ Normalizes target probability distribution """

        integral = np.sum(self.mu) * self.dx * self.dy

        self.mu = self.mu / integral

        return 

    def compute_mu_k(self):
        """" Computes Fourier coefficients of probability distribution """

        if self.mu_k_current:
            return

        # first normalize target probability distribution
        self.normalize_mu()

        self.mu_k = (dct(dct(self.mu.T, norm=None).T / 2.0, norm=None) / 2.0) * self.dx * self.dy

        self.mu_k_current = True

        return

    def set_zero(self):
        """ Sets all values in mu probdist array to zero """

        self.mu = np.zeros((self.Nx, self.Ny))

        self.mu_k_current = False

        return

    def set_value_in_rect(self, rect_xmin, rect_xmax, rect_ymin, rect_ymax, value):
        """ Sets the probability distribution in the specified rectangle to the given value """

        for i, j in product(range(self.Nx), range(self.Ny)):

            x = self.xmin + i * self.dx
            y = self.ymin + j * self.dy

            if rect_xmin <= x <= rect_xmax and rect_ymin <= y <= rect_ymax:

                self.mu[i, j] = value

        self.mu_k_current = False

        return

    def set_value_in_ellipse(self, xc, yc, a, b, value):
        """ Sets the probability distribution in the specified ellipse to the given value """

        for i, j in product(range(self.Nx), range(self.Ny)):

            x = self.xmin + i * self.dx
            y = self.ymin + j * self.dy

            ellipse_check = (x - xc) ** 2.0 / a ** 2.0 + (y - yc) ** 2.0 / b ** 2.0

            if ellipse_check <= 1.0:
                self.mu[i, j] = value

        self.mu_k_current = False

        return

    def set_value_in_circle(self, xc, yc, radius, value):
        """ Sets the probability distribution in the specified circle to the given value """

        for i, j in product(range(self.Nx), range(self.Ny)):

            x = self.xmin + i * self.dx
            y = self.ymin + j * self.dy

            circle_check = ((x - xc) ** 2.0 + (y - yc) ** 2.0) / radius ** 2.0

            if circle_check <= 1.0:
                self.mu[i, j] = value

        self.mu_k_current = False

        return

    def set_prob_dist_from_array(self, array):
        """ Sets the probability distribution from given array """

        if self.Nx != array.shape[0] and self.Ny != array.shape[1]:
            print('Warning: array shape not same shape as probdist grid, Probdist not updated!')
            return

        for i, j in product(range(self.Nx), range(self.Ny)):

            self.mu[i, j] = array[i, j]

        self.mu_k_current = False

        return

    def set_prob_dist_on_curve(self, parametric_curve, parameter_range):
        """ Sets a dirac-like distribution on the given parametric curve """

        Nx = self.Nx
        Ny = self.Ny

        Lx = self.xmax - self.xmin
        Ly = self.ymax - self.ymin
        xmin = self.xmin
        ymin = self.ymin

        self.mu_k = np.zeros((self.Nx, self.Ny))
        for parameter in parameter_range:
            (xpos, ypos) = parametric_curve(parameter)
            (xrel, yrel) = (xpos - xmin, ypos - ymin)
            for kx, ky in product(range(Nx), range(Ny)):
                self.mu_k[kx, ky] += cos(kx * pi * xrel / Lx) * cos(ky * pi * yrel / Ly)

        self.mu_k = self.mu_k / (float(len(parameter_range)))

        self.mu_k_current = True

        return

    def add_gaussian(self, mu, cov, weight):
        """
        Adds a gaussian density of given mean and covariance and with given weight
        """

        pdf = partial(pdf_multivariate_gauss, mu=mu, cov=cov)

        for i, j in product(range(self.Nx), range(self.Ny)):

            x = self.xmin + i * self.dx
            y = self.ymin + j * self.dy

            self.mu[i, j] += weight * pdf(np.array([[x], [y]]))

        self.mu_k_current = False

        return


def pdf_multivariate_gauss(x, mu, cov):
    """
    Calculate the multivariate normal density (pdf)

    Arguments:
        x = numpy array of a "d x 1" sample vector
        mu = numpy array of a "d x 1" mean vector
        cov = "numpy array of a d x d" covariance matrix
    """

    assert(mu.shape[0] > mu.shape[1]), 'mu must be a row vector'
    assert(x.shape[0] > x.shape[1]), 'x must be a row vector'
    assert(cov.shape[0] == cov.shape[1]), 'covariance matrix must be square'
    assert(mu.shape[0] == cov.shape[0]), 'cov_mat and mu_vec must have the same dimensions'
    assert(mu.shape[0] == x.shape[0]), 'mu and x must have the same dimensions'

    part1 = 1 / ( ((2* np.pi)**(len(mu)/2)) * (np.linalg.det(cov)**(1/2)) )
    part2 = (-1/2) * ((x-mu).T.dot(np.linalg.inv(cov))).dot((x-mu))

    return float(part1 * np.exp(part2))


