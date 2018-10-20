
### Generate watercolor-like paintings

*Dyamic SMC* can be used to generate watercolor-like paintings. One such example is shown below.

```python
# After necessary imports
# Read image and convert to density
image = imread('lady_painting.jpg')
image_dens = 255.0 - image.T
image_dens = np.fliplr(image_dens)

# Define probability distribution
xmin, ymin = (0, 0)
xmax, ymax = image_dens.shape
prob_dist = ProbDist(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, Nx=xmax, Ny=ymax)
prob_dist.set_prob_dist_from_array(image_dens)

# setting up simulation parameters
n_agents = 20
n_time_steps = 10000
paint_rate = sum(sum(image_dens)) / float(n_time_steps * n_agents)

# initializing paint density array
paint_dens = np.zeros(image_dens.shape)

# Define DynamicSMC coverage object
dynamic_smc = DynamicSMC(prob_dist)

# add agents to coverage object
for _ in range(n_agents):
    dynamic_smc.add_agent(Agent(xmin + random.random() * (xmax-xmin),
    				ymin + random.random() * (ymax-ymin)))

# Run the algorithm 
for time_ind in range(n_time_steps):

    dynamic_smc.time_steps(1, 1.0)

    # code here to use current agent locations for updating 
    # paint density array and display

```
Below is shown an animation of the evolving painting. To see the full code for this example, look [here](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_painting.py). The original painting used for this experiment is this: ![lady_painting](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/lady_painting.jpg?raw=true). More complex and color paintings can be generated using *Dynamic SMC* as seen in this [paper](https://arxiv.org/abs/1504.02010). 

Evolving painting          |  Final painting
:-------------------------:|:-------------------------:
![dynamic_smc_painting](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_painting.gif?raw=true)  |  ![dynamic_smc_painting_final](https://github.com/qpcode/smc/blob/master/examples/dynamic_smc/dynamic_smc_painting_final.jpg?raw=true)


