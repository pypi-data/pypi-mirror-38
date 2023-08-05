====
scVI
====

.. image:: https://travis-ci.org/YosefLab/scVI.svg?branch=master
    :target: https://travis-ci.org/YosefLab/scVI

.. image:: https://codecov.io/gh/YosefLab/scVI/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/YosefLab/scVI

.. image:: https://readthedocs.org/projects/scvi/badge/?version=latest
        :target: https://scvi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Single-cell Variational Inference

* Free software: MIT license
* Documentation: https://scvi.readthedocs.io.


Quick Start
-----------

1. Install Python 3.6 or later. We typically use the Miniconda_ Python distribution.

.. _Miniconda: https://conda.io/miniconda.html

2. Install PyTorch_. If you have an Nvidia GPU, be sure to install a version of PyTorch that supports it -- scVI runs much faster with a discrete GPU.

.. _PyTorch: http://pytorch.org

3. Install ``scvi`` through conda (``conda install scvi -c bioconda``) or through pip (``pip install scvi``). Alternatively, you may clone this repository and manually install the dependencies listed in setup.py_.

.. _setup.py: https://github.com/YosefLab/scVI/tree/master/setup.py


4. Refer to `this Jupyter notebook`__ to see how to import datasets into scVI.

.. __: https://github.com/YosefLab/scVI/tree/master/tests/notebooks/data_loading.ipynb

5. Refer to `this Jupyter notebook`__ to see how to train the scVI model, impute missing data, detect differential expression, and more!

.. __: https://github.com/YosefLab/scVI/tree/master/tests/notebooks/basic_tutorial.ipynb


References
----------

Romain Lopez, Jeffrey Regier, Michael Cole, Michael I. Jordan, Nir Yosef.
**"Deep generative modeling for single-cell transcriptomics"**
Nature Methods, in press (accepted Oct 26, 2018). 
Preprint available at https://www.biorxiv.org/content/early/2018/03/30/292037
