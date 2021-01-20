
![badge-OS](https://img.shields.io/badge/OS-Windows-blue)
![badge-language](https://img.shields.io/badge/language-Python-blue)
![badge-license](https://img.shields.io/badge/license-GNU-blue)

Support this project and keep always updated about recent software releases, bug fixes and major improvements by [following on github](https://github.com/dpscience?tab=followers).

![badge-followers](https://img.shields.io/github/followers/dpscience?style=social)
![badge-stars](https://img.shields.io/github/stars/dpscience/DCONTINPALS?style=social)
![badge-forks](https://img.shields.io/github/forks/dpscience/DCONTINPALS?style=social)

# pyDCONTINPALS

Copyright (c) 2020-2021 Danny Petschke (danny.petschke@uni-wuerzburg.de). All rights reserved.<br><br>
<b>pyDCONTINPALS</b> - A program in Python for running the historical FORTRAN code CONTIN-PALS initially provided by [Provencher (1982)](https://www.sciencedirect.com/science/article/abs/pii/0010465582901746) and [Gregory et al. (1990/](https://www.sciencedirect.com/science/article/abs/pii/016890029090358D)[1991)](https://www.sciencedirect.com/science/article/abs/pii/016890029190367Y). CONTIN-PALS program solves Fredholm integral equations with convoluted exponential decays as kernels of the type that occur in the analysis of Positron Annihilation Lifetime Spectra (PALS).<br>

![demo](/demo.png)

# Quickstart Guide

`pyDCONTINPALS` consists of 3 files ...<br>

`pyDCONTINPALS.py`<br>
`pyDCONTINPALSInput.py`<br>
`pyDCONTINPALSSpecSimulator.py`<br>

* <b>edit</b> the input file `pyDCONTINPALSInput.py`:

```python
__demoMode                  = True # disable if running from real data

# NOTE: spectrum and IRF (or mono-exponential decay spectrum e.g. 207-Bi) data vectors require equal length!

# file path (and name) to the SPECTRUM data:
__filePathSpec              = 'testData/spectrum_10ps.dat'
__specDataDelimiter         = '\t'

# file path (and name) to the IRF data:
__filePathRefOrIRFSpec      = 'testData/ref_10ps.dat'
__refDataDelimiter          = '\t'

# define the number of rows, which should be skipped during the import (e.g. for ignoring the header entries):
__skipRows                  = 5;

# fixed mono-decay component in units of picoseconds [ps] (1/lambda = tau):
# Note: set to something like 1E-6 if you provide numerical IRF data as input such as recorded from 60-Co
__tau_monoDecaySpec_in_ps   = 182.0  #[ps]

# grid of characteristic lifetimes with equally distributed grid points defining the resulting intensity spectrum
__gridTau_start             = 50.0   # [ps]
__gridTau_stop              = 3000.0 # [ps]
__gridPoints                = 100    # 10 ... 100 Note: this value is internally limited to 100 by CONTIN

# channel/bin resolution [ps]
__channelResolutionInPs     = 50.0  # >= 10 ... Note: this value is internally limited by CONTIN

# background estimation:
__bkgrd_startIndex          = 800;
__bkgrd_count               = 190; # number of channels with respect to the 'startIndex'
```
* <b>execute</b> `pyDCONTINPALS.py`<br>

* <b>finished</b>. You should see the results as shown above in the figures when running in the demo mode <i>(__demoMode = True)</i>.

# How to cite this Program?

* <b>Before citing this program <b>pyDCONTINPALS</b> you need at least to cite the initial publication of the FORTRAN program [CONTIN-PALS provided by Gregory et al. (1990)](https://www.sciencedirect.com/science/article/abs/pii/016890029090358D).</b>

[![DOI](https://img.shields.io/badge/DOI-10.1016%2F0168--9002(90)90358--D-yellowgreen)](https://www.sciencedirect.com/science/article/abs/pii/016890029090358D)

[R.B. Gregory, Y. Zhu, Analysis of positron annihilation lifetime data by numerical laplace inversion with the program CONTIN, Nucl. Instruments Methods Phys. Res. Sect. A Accel. Spectrometers, Detect. Assoc. Equip. 290 (1990) 172–182. doi:10.1016/0168-9002(90)90358-D.](https://doi.org/10.1016/0168-9002(90)90358-D).

* <b>Additionally, you should cite the applied version of this program in your study.</b><br>

You can cite all released software versions by using the <b>DOI 10.5281/zenodo.3665474</b>. This DOI represents all versions, and will always resolve to the latest one.<br>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3665474.svg)](https://doi.org/10.5281/zenodo.3665475)

## ``v1.x``
<b>pyDCONTINPALS v1.01</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4452238.svg)](https://doi.org/10.5281/zenodo.4452238)<br>
<b>pyDCONTINPALS v1.0</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3665475.svg)](https://doi.org/10.5281/zenodo.3665475)<br>
 
 # License of (py)DCONTINPALS (GNU General Public License) 
 Copyright (c) 2020-2021 Danny Petschke (danny.petschke@uni-wuerzburg.de) All rights reserved.<br><br>

<p align="justify">This program is free software: you can redistribute it and/or modify<br>
it under the terms of the GNU General Public License as published by<br>
the Free Software Foundation, either version 3 of the License, or<br>
(at your option) any later version.<br><br>

This program is distributed in the hope that it will be useful,<br>
but WITHOUT ANY WARRANTY; without even the implied warranty of<br>
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.<br><br></p>

For more details see [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0)
