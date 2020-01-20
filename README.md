## Prerequisites

### Essentials
`Python 3.6` or higher with `pip`
These should be installed on most systems, if not, detailed guides depending on operating system can be found in the Internets.

### Creating virtual environment (optional by highly recommended)
From project folder run 
```python3 -m venv .env-stickleback-agent-base-decisionmaking```
to create a virtual environment.

To active the environment, run:
 ```source .env-stickleback-agent-base-decisionmaking/bin/activate```

### Installing python libraries
Run 
```pip3 install -r requirements.txt```
to install python libraries, used in this project.

### Installing glfw
`p5` library, used to visualize the simulations, depends on `glfw`. Detailed installation instructions depending on your operating system can be found [here](https://p5.readthedocs.io/en/latest/install.html).

## Running simulations
To run simulation with basic parameters, run 
```python3 main.py```

The following parameters can be used:
```
--max-steps \\ max steps to run simulation
```
To run with parameter just specify them in command using suitable values, e.g.:

```
python3 main.py --max-steps=2000
```