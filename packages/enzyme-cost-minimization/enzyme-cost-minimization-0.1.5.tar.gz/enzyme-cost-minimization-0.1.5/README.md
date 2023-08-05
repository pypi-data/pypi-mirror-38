enzyme-cost-minimization
========================

Enzyme Cost Minimization (ECM) is a method for estimating the specific cost in 
enzymes for sustaining a given flux, given a kinetic model.

You can read more about ECM at [PLOS CB](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5094713/).

If you only want to try out ECM without installing anything locally, we have
a simple web interface at [eQuilibrator](http://equilibrator.weizmann.ac.il/pathway/).

Otherwise, you can install ECM from PyPI:
```
pip install enzyme-cost-minimization
```

Or get the source code from this repository. In that case, you'll have to 
install the following dependencies:
- PyPI packages:
    - numpy
    - scipy
    - matplotlib
    - optlang
    - pandas
    - sbtab
    - equilibrator-api
    
Example
-------
Try running the example script:
```
python -m example.test
```
