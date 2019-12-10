FROM continuumio/miniconda3
MAINTAINER Alex Lubbock <code@alexlubbock.com>

RUN conda install -c alubbock pysb kappa stochkit nfsim atomizer matplotlib pandas cython
RUN apt-get update && apt-get install -y gcc
RUN mkdir /pysb
ADD pysb-garuda.py /pysb/
ENTRYPOINT ["python", "/pysb/pysb-garuda.py"]
