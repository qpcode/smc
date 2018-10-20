
### Dynamic Coverage of a bimodal distribution

Here is an example of *Dyamic SMC* used to explore a bimodal distribution. 

```python
# After necessary imports
# Define probability distribution
xmin, xmax = (-100.0, 100.0)
ymin, ymax = (-100.0, 100.0)
prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=100, Ny=100)
# first set everything to zero
prob_dist.set_zero()

# adding first gaussian distribution 
prob_dist.add_gaussian(mu_1, cov_1, 1.0)

# adding second gaussian distribution
prob_dist.add_gaussian(mu_2, cov_2, 1.0)

# Define StaticSMC coverage object
dynamic_smc = DynamicSMC(prob_dist)

# Add agents (with random initial locations) to coverage object
for _ in range(10):
    random_state = (xmin + (xmax - xmin) * random.random(),
                    ymin + (ymax - ymin) * random.random())
    dynamic_smc.add_agent(Agent(random_state[0], random_state[1]))

# Run the algorithm (1000 time-steps of size 1)
dynamic_smc.time_steps(1000, 1) 
```
Below is shown an animation of the trajectories exploring the bimodal distribution using *Dynamic SMC*. The green coloring represents the bimodal distribution to be covered. To see the full code for this example, look [here](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_bimodal.py).

![dynamic_smc_bimodal](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_bimodal.gif?raw=true)
