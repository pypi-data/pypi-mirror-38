[![Build Status](https://travis-ci.org/sanbales/ipython-coverage.svg?branch=master)](https://travis-ci.org/sanbales/ipython-coverage)

# IPython Coverage
Introduces `%coverage` and `%%coverage` magics to allow running
of [coverage](https://github.com/nedbat/coveragepy)
from a [Jupyter Notebook](https://github.com/jupyter/notebook).

It currently presents the coverage HTML report as an IFrame.

# Installation
```bash
pip install ipycoverage
```

# Usage

## Load the extension
```ipython
%load_ext ipycov
```

## Use the magic
In a cell, you can run the cell magic like such:
```ipython
%%coverage
from your_module import your_function  # or anything else you want to import

your_function()
```

twine register dist/pad-on-left-1.0.0.tar.gz -r testpypi

Or simply run the line magic:
```ipython
%coverage function_to_call()
``` 

# Important Note
> This is not a fully developed magic, and it is not stable yet.
>
> It has only been tested against:
> * `coverage==4.5.2`
> * `IPython==7.0.1`.
> * `JupyterLab==0.35.1`

## Missing Features / Future Work
* Improve naming and instructions
* Add more options; potentially dynamically load them from `coverage`
* Add tests
* Add examples
* Add CI/CD
* Submit to PyPI and Conda
