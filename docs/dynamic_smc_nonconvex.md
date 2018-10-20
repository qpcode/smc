
### Dynamic Coverage of non-convex domains

Here is an example of *Dyamic SMC* used to explore a non-convex domain.

```python
# After necessary imports
# Define probability distribution
xmin, xmax = (-100.0, 100.0)
ymin, ymax = (-100.0, 100.0)
prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=100, Ny=100)

# first set everything to zero
prob_dist.set_zero()

# set distribution on ring and square
prob_dist.set_value_in_circle(0.0, 0.0, 75.0, 1.0)
prob_dist.set_value_in_circle(0.0, 0.0, 60, 0.0)
prob_dist.set_value_in_rect(-20, 20, -20, 20, 1.0)

# Define DynamicSMC coverage object
dynamic_smc = DynamicSMC(prob_dist)

# Add agents (with random initial locations) to coverage object
for _ in range(25):
    random_state = (xmin + (xmax - xmin) * random.random(),
                    ymin + (ymax - ymin) * random.random())
    dynamic_smc.add_agent(Agent(random_state[0], random_state[1]))

# Run the algorithm (1000 time-steps of size 1)
dynamic_smc.time_steps(1000, 1) 
```
Below is shown an animation of the trajectories exploring the union of a ring and a square using *Dynamic SMC*. The blue coloring represents the domain to be covered. To see the full code for this example, look [here](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_nonconvex.py).

![dynamic_smc_nonconvex](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_nonconvex.gif?raw=true)
