
### Covering a domain with holes

Say you wanna cover a domain with holes using a large number of agents. Here is how you can use *Static SMC* to do so.

```python
# After necessary imports
# Define probability distribution
prob_dist = ProbDist(xmin=0.0, xmax=1.0, ymin=0.0, ymax=1.0)

# Add rectangular hole to domain
prob_dist.set_value_in_rect(0.2, 0.5, 0.7, 0.8, 0.0)

# Add elliptical hole to domain
prob_dist.set_value_in_ellipse(0.7, 0.3, 0.2, 0.1, 0.0)

# Define StaticSMC coverage object
static_smc = StaticSMC(prob_dist)

# Add agents (with random initial locations) to coverage object
for _ in range(1000):
    static_smc.add_agent(Agent(random.random(), random.random()))

# Run the algorithm (100 time-steps of size 0.001)
static_smc.time_steps(100, 0.001) 
```
Below is shown the initial random locations of the agents and the final optimal configuration obtained using *Static SMC*. To see the full code for this example, look [here](https://github.com/qpcode/smc/blob/master/examples/static_smc/static_smc_1000.py).

![static_smc_3x3](https://github.com/qpcode/smc/blob/master/examples/static_smc/static_smc_1000.png?raw=true)
