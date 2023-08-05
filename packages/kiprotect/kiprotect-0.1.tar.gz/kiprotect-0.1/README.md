[![Build Status](https://travis-ci.org/7scientists/rouster.svg?branch=master)](https://travis-ci.org/7scientists/rouster)

# Welcome!

Rouster is a docker-based tool for building reproducible data anylsis workflows.

Currently the code in this repository is still evolving rapidly as we're working towards
a first stable version. If you have any feedback, suggestions, ideas or feature requests,
please feel free to [open an issue](https://github.com/7scientists/rouster/issues).

Thanks!

# Installation

To install the dependencies, use the following command:

    pip install -r requirements.txt --find-links=dependencies

This will make sure that Pip looks in the dependencies directory for missing packages
(currently the `docker` package on Pypi is broken so we install it from a wheel generated
using the master branch)
