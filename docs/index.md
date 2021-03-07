
Introduction
------------

SMC provides a suite of algorithms meant to solve various coverage problems using multi-agent systems. SMC is a simple yet effective approach for solving such coverage problems. The algorithms in this library are primarily based on ideas presented in these two papers:

1. [A Static Coverage Algorithm for Locational Optimization](https://static1.squarespace.com/static/5eea6362f2f0d46ceceba388/t/5ef04495560a724a67897faf/1592804503616/Static_SMC_CDC.pdf)
2. [Metrics for ergodicity and design of ergodic dynamics for multi-agent systems](https://static1.squarespace.com/static/5eea6362f2f0d46ceceba388/t/5ef04406111d8b59195003c5/1592804370071/Mathew10Metrics.pdf)

Download and Install
--------------------

To download the smc repository simply do:
```shell
git clone https://github.com/qpcode/smc.git
```
To install the smc package, go into the smc repo directory and simply do:
```shell
python setup.py install
```
Use ```sudo``` based on whether you want to install the package as a superuser. Also, in case your machine doesn't satisfy the requirements, create a [virtualenv](https://docs.python-guide.org/dev/virtualenvs/), activate it and then install the smc requirements by going into the smc repo directory and doing:
```shell
pip install -r requirements.txt
```

Static Coverage problems
------------------------

The first kind of coverage problem is where one is interested finding a static configuration of agents that is optimized for coverage of a probability distribution. For example, if one wants to place 9 agents that optimally cover a uniform distribution on a square domain, here is how one can do it with *Static SMC*.  
```python
# After necessary imports
# Define probability distribution and StaticSMC object
prob_dist = ProbDist(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0)
static_smc = StaticSMC(prob_dist)

# Add agents (with random initial locations) to coverage object
for iagent in range(9):
    static_smc.add_agent(Agent(random.random(), random.random()))

# Run the algorithm (2000 time-steps of size 0.01)
static_smc.time_steps(2000, 0.01) 
```
Below is shown the random initial locations of the agents together with the final optimal configuration obtained using *Static SMC*. As can be seen, the agents get naturally arranged in an approximate 3 X 3 grid. To see the full code for this example, look [here](https://github.com/qpcode/smc/blob/master/examples/static_smc/static_smc_3x3.py).


![static_smc_3x3](https://github.com/qpcode/smc/blob/master/examples/static_smc/static_smc_3x3.png?raw=true)

Here is a listing of other static coverage examples:

1. [Static Coverage of a Gaussian distribution.](static_smc_gaussian.md)
2. [Static Coverage of domains with holes.](static_smc_holes.md)
3. [Static Coverage of curves.](static_smc_curves.md)
4. [Generate Pointillism art.](static_smc_pointillism.md)

Solving various coverage problems boils down to setting up interesting probability distributions. To see how to set up interesting probability distributions, see the API for the [ProbDist class](https://github.com/qpcode/smc/blob/master/smc/probdist.py). 

Dynamic Coverage problems
-------------------------

These kind of coverage problems arise when one is interested in planning trajectories for agents so that they visit (or come close to visiting) every single point in the domain. For example, if one wants to plan trajectories for four agents so that they explore a square domain uniformly, one can do it with *Dynamic SMC* as follows:

```python
# After necessary imports
# Define probability distribution and DynamicSMC object
prob_dist = ProbDist(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0)
dynamic_smc = DynamicSMC(prob_dist)

# Add agents (with random initial locations) to coverage object
for iagent in range(4):
    dynamic_smc.add_agent(Agent(random.random(), random.random()))

# Run the algorithm (1000 time-steps of size 0.01)
trajectories = dynamic_smc.time_steps(1000, 0.01, return_trajectories=True) 
```

The left and right figures below shown the trajectories after 500 time-steps and 1000-time-steps respectively. As can be seen, the gaps left between trajectories become smaller as time proceeds. To see the full code for this example, look [here](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_4agents.py).

![dynamic_smc_4agents](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_4agents.png?raw=true)

Here is a listing of other dynamic coverage examples:

1. [Dynamic Coverage of a bimodal distribution.](dynamic_smc_bimodal.md)
2. [Dynamic Coverage of a non-convex domain.](dynamic_smc_nonconvex.md)
3. [Dynamic Coverage of a moving target distribution.](dynamic_smc_moving_target.md)
4. [Generate watercolor-like paintings.](dynamic_smc_painting.md)

Related Work
------------

Some links to related work are provided below:

1. [Ergodic Exploration of Distributed Information](https://arxiv.org/abs/1708.09352).
2. [Autonomous Visual Rendering using Physical Motion](https://arxiv.org/abs/1709.02758).
3. [Multi-Agent Ergodic Coverage with Obstacle Avoidance](http://biorobotics.ri.cmu.edu/papers/paperUploads/15731-68931-1-PB.pdf).
4. [A Julia package for generating ergodic trajectories using projection-based optimization and smc](https://github.com/dressel/ErgodicControl.jl)

Contact
-------

For any questions or ideas regarding this library, contact me at ergodicrobots@gmail.com
