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

## Running simulations with UI
To run simulation with basic parameters (2 fishes, no replicas), run 
```python3 simulation.py```

The following parameters can be used:
```
-f (--fishes) - number of fishes
-t (--replicas-top) - number of replicas on top 
-b (--replicas-bottom) - number of replicas in the bottom
-r (--free-run) - free run mode, with no experimental setup
```
To run with parameters, specify them in command line e.g.:

```
python3 simulation.py --fishes=4 --replicas=2 \\ run with 4 fishes and 2 replicas
python3 simulation.py --fishes=8 \\ run with 8 fishes (2 replicas will be set by default)
python3 simulation.py -r=1 \\ run in free run mode (no experimental set)
```

## Running simulations from python console
You can use `python` (or `ipython`) to run simulation from console

In this case UI will not be triggered, simulations run faster and finish when all fishes make their decisions

Function `main.headless_simulation` receives two key parameters: `fishes` and `replicas`. It returns a tuple with number of fishes, that selected top and fishes, that selected bottom.

Function `main.headless_simulations` receives three key parameters: `shoals` (NB: the same as times simulation will run), `fishes` and `replicas`. 
It returns a tuple, where each element corresponds to one shoal and it's value is a proportion of fishes, that went top.
