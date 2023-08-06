<img src="inst/extdata/deploid.png" width="180">

[![License (GPL version 3)](https://img.shields.io/badge/license-GPL%20version%203-brightgreen.svg)](http://opensource.org/licenses/GPL-3.0)
[![Build Status](https://travis-ci.org/DEploid-dev/DEploid-py.svg?branch=master)](https://travis-ci.org/DEploid-dev/DEploid-py)
[![Documentation Status](https://readthedocs.org/projects/deploid-py/badge/?version=latest)](https://deploid-py.readthedocs.io/en/latest/?badge=latest)

DEploid Python package -- Deconvolute Mixed Genomes with Unknown Proportions
=================

Traditional ‘phasing’ programs are limited to diploid organisms. Our method modifies Li and Stephen’s algorithm with Markov chain Monte Carlo (MCMC) approaches, and builds a generic framework that allows haloptype searches in a multiple infection setting.

Installation

```bash
pip install dEploid
```

Usage
-----

Please see the [documentation](https://deploid-py.readthedocs.io/en/latest/) for further details.


Licence
-------

You can freely use all code in this project under the conditions of the GNU GPL Version 3 or later.


Citation
--------

If you use `dEploid` with the flag `-ibd`, please cite the following paper:

Zhu, J. S., J. A. Hendry, J. Almagro-Garcia, R. D. Pearson, R. Amato, A. Miles, D. J. Weiss, T. C. D. Lucas, M. Nguyen, P. W. Gething, D. Kwiatkowski, G. McVean, and for the Pf3k Project. (2018) The origins and relatedness structure of mixed infections vary with local prevalence of *P. falciparum* malaria. *biorxiv*, doi: https://doi.org/10.1101/387266.


If you use `dEploid` in your work, please cite the program:

Zhu, J. S. J. A. Garcia G. McVean. (2018) Deconvolution of multiple infections in *Plasmodium falciparum* from high throughput sequencing data. *Bioinformatics* 34(1), 9-15. doi: https://doi.org/10.1093/bioinformatics/btx530.


