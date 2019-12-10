# PySB-in-Docker for use in pipelines

This repository wraps [PySB](https://github.com/pysb/pysb)
in a Docker container for deployment in automated pipelines.

A model is loaded (SBML or PySB format) then simulated through
one of PySB's simulators, which include multiple ODE integrators
and stochastic simulation algorithms.

## Usage

    docker pull alubbock/pysb-garuda
    docker run --rm alubbock/pysb-garuda

The last command will show help with available arguments.

## Examples

Download and run BioModels model
[BIOMD0000000001](http://www.ebi.ac.uk/biomodels-main/BIOMD0000000001)
using the default VODE integrator for 11 seconds of integration time,
from 0 to 10 seconds:

    docker run --rm alubbock/pysb-garuda --biomodels 1 --tlen 11 --tmax 10

Run a PySB JSON model using StochKit, 3 realizations:

    docker run --rm -v /path/to/file.json:/model.json alubbock/pysb-garuda --json-model /model.json --tlen 11 --tmax 10 --simulator StochKitSimulator --nruns=3

Run an SBML model using NFsim through BioNetGen, 5 realizations:

    docker run --rm -v /path/to/file.sbml:/model.sbml alubbock/pysb-garuda --sbml-model /model.sbml --tlen 11 --tmax 10 --simulator BngSimulator --method=nf --nruns=5
