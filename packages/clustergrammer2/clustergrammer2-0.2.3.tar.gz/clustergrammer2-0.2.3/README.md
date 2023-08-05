
# clustergrammer2

[![Build Status](https://travis-ci.org/ismms-himc/clustergrammer2.svg?branch=master)](https://travis-ci.org/ismms-himc/clustergrammer2)
[![codecov](https://codecov.io/gh/ismms-himc/clustergrammer2/branch/master/graph/badge.svg)](https://codecov.io/gh/ismms-himc/clustergrammer2)


A custom Jupyter widget library built using the widget-ts-cookiecutter library'

## Installation

A typical installation requires the following commands to be run:

```bash
pip install clustergrammer2
jupyter nbextension enable --py [--sys-prefix|--user|--system] clustergrammer2
```

Or, if you use jupyterlab:

```bash
pip install clustergrammer2
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

## Running Locally

### widget-ts-cookiecutter release instructions
The release instructions from the [jupyter-widgets/widget-ts-cookiecutterREADME](https://github.com/jupyter-widgets/widget-ts-cookiecutter).

#### Webpack

This will build the bundle, then build the nbextension and labextension:

```
  npm run watch
  npm run build:all

```