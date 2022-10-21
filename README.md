# 3-omega
## Description
A simulated look at the 3-omega technique for the measurement of thermal conductivity as found in the blog-post <https://microncubed.com/simulating-measurements-of-thermal-conductivity/>. In brief, I simulate the ac thermal response of a glass substrate and log the in-phase component of temperature variation as a function of frequency. From this, it is possible to fit the thermal conductivity which is reasonably close to the input value. This proved to be an interesting way to learn more about the 3-omega technique.

## Files
There is one Jupyter notebook 01_run_simulations.ipynb in the scripts folder. It draws code from the src folder, outputs into the data and figures folders. In the src folder we have the simulation code (pdeSim.py), a models file (models.py) and a table of thermal parameters (thermal_properties.csv).