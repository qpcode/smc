
### Pointillism

Yes, you can do fun stuff like generating pointillism art from photographs. Here is a simple example.

```python
# After necessary imports
# Read image and convert to density
image = imread('heisenberg.jpg')
image_dens = 255.0 - image.T
image_dens = np.fliplr(image_dens)

# Define probability distribution
xmin, ymin = (0, 0)
xmax, ymax = image_dens.shape
prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=xmax, Ny=ymax)
prob_dist.set_prob_dist_from_array(image_dens)

# Define StaticSMC coverage object
static_smc = StaticSMC(prob_dist)

# Add agents (with random initial locations) to coverage object
for _ in range(2000):
    static_smc.add_agent(Agent(random.random(), random.random()))

# Run the algorithm (150 time-steps of size 0.125)
static_smc.time_steps(150, 0.125) 
```

The animation below shows the positions of the agents evolving to a configuration representing the image. To see the full code for generating this animation, look [here](https://github.com/qpcode/smc/blob/master/examples/static_smc/static_smc_pointillism.py). The original Heisenberg image used for this experiment is this: ![heisenberg](https://github.com/qpcode/smc/blob/master/examples/static_smc/heisenberg.jpg?raw=true)

##### smc pointillism applied to Heisenberg image 
![static_smc_pointillism](https://github.com/qpcode/smc/blob/master/examples/static_smc/static_smc_pointillism.gif?raw=true)