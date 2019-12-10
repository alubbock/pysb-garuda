from __future__ import print_function
import argparse
import sys
import pysb.simulator
from pysb.simulator.bng import BngSimulator
from pysb.importers.sbml import model_from_sbml, model_from_biomodels
from pysb.importers.json import model_from_json
import numpy as np

# Set up the argparser
SIMULATOR_CHOICES = ('ScipyOdeSimulator', 'StochKitSimulator', 'BngSimulator',
                     'KappaSimulator')
BNG_SIM_TYPES = BngSimulator._SIMULATOR_TYPES

parser = argparse.ArgumentParser(description='PySB Garuda Integration')
input_group = parser.add_mutually_exclusive_group(required=True)
input_group.add_argument('--sbml-model',
                         help='An SBML format model file to import')
input_group.add_argument('--biomodels',
                         help='Download a model from BioModels as input')
input_group.add_argument('--json-model',
                         help='PySB model in JSON format as input')
parser.add_argument('--output',
                    help='Output filename for simulation results (CSV); '
                         'defaults to stdout',
                    required=False)
parser.add_argument('--simulator',
                    help='Simulation engine',
                    choices=SIMULATOR_CHOICES,
                    default='ScipyOdeSimulator')
parser.add_argument('--tlen',
                    type=int,
                    help='Number of time points in simulation',
                    required=True)
parser.add_argument('--tmax',
                    type=float,
                    help='Final time of simulation',
                    required=True)
parser.add_argument('--method',
                    type=str,
                    choices=BNG_SIM_TYPES,
                    required=False)
parser.add_argument('--nruns', type=int, default=1)

# Parse arguments and validate
args = parser.parse_args()


def _exit(message, exit_code=2):
    print(message, file=sys.stderr)
    sys.exit(exit_code)

try:
    sim_class = getattr(pysb.simulator, args.simulator)
except AttributeError:
    _exit('Unknown Simulator: "{}"\nChoices are: {}'.format(
        args.simulators,
        ", ".join(SIMULATOR_CHOICES)
    ))

run_kwargs = {}

if args.method is not None:
    if args.simulator != 'BngSimulator':
        _exit("--method can only be used with BngSimulator")
    run_kwargs['method'] = args.method

if args.nruns > 1:
    if args.simulator == 'ScipyOdeSimulator':
        _exit('ScipyOdeSimulator doesn\'t support nruns > 1')
    run_kwargs['n_runs'] = args.nruns

# Load the model
if args.json_model:
    model = model_from_json(args.json_model)
elif args.biomodels:
    model = model_from_biomodels(args.biomodels)
else:
    model = model_from_sbml(args.sbml_model)

# Create the simulator
sim = sim_class(model=model, tspan=np.linspace(0, args.tmax, args.tlen))

# Run the simulation(s)
res = sim.run(**run_kwargs)

# Save the results to CSV
res.dataframe.to_csv(sys.stdout if args.output is None else args.output)
