![badge-OS](https://img.shields.io/badge/OS-tested%20under%20Windows%2010-brightgreen)
![badge-OS](https://img.shields.io/badge/OS-tested%20under%20Windows%2011-brightgreen)

Support this project and keep always updated about recent software releases, bug fixes and major improvements by [following on github](https://github.com/dpscience?tab=followers).

![badge-followers](https://img.shields.io/github/followers/dpscience?style=social)
![badge-stars](https://img.shields.io/github/stars/dpscience/DCONTINPALS?style=social)
![badge-forks](https://img.shields.io/github/forks/dpscience/DCONTINPALS?style=social)

# pyDCONTINPALS

![badge-OS](https://img.shields.io/badge/OS-Windows-blue)
![badge-language](https://img.shields.io/badge/language-Python-blue)
![badge-license](https://img.shields.io/badge/license-GPL-blue)

Copyright (c) 2020-2022 Dr. Danny Petschke (danny.petschke@uni-wuerzburg.de). All rights reserved.<br><br>
<b>pyDCONTINPALS</b> - A program in Python for running the historical FORTRAN code CONTIN-PALS initially provided by [Provencher (1982)](https://www.sciencedirect.com/science/article/abs/pii/0010465582901746) and [Gregory et al. (1990/](https://www.sciencedirect.com/science/article/abs/pii/016890029090358D)[1991)](https://www.sciencedirect.com/science/article/abs/pii/016890029190367Y). CONTIN-PALS program solves Fredholm integral equations with convoluted exponential decays as kernels of the type that occur in the analysis of Positron Annihilation Lifetime Spectra (PALS).<br>

![demo](https://github.com/dpscience/DCONTINPALS/blob/cef7dea07b87d1b878eec602a3c070a8d5555636/demo.png)

# Quickstart Guide

`pyDCONTINPALS` consists of 3 files ...<br>

`pyDCONTINPALS.py`<br>
`pyDCONTINPALSInput.py`<br>
`pyDCONTINPALSSpecSimulator.py`<br>

* <b>edit</b> the input file `pyDCONTINPALSInput.py`:

```python
__demoMode                  = True # disable if running from real data

# NOTE: SPECTRUM and IRF (or mono-exponential decay spectrum) data vectors require equal length!

__roi_start                 = 0
__roi_end                   = 7400 # Note: number of channels is internally limited by CONTIN to <= 4000, so adjust the '__binFactor' in order to fit the given number of channels into this range

# file path (and name) to the SPECTRUM data:

__usingRefSpectrum          = True # if set to FALSE the '__irfXXX' related parameters are considered

__filePathSpec              = 'testData/spectrum_10ps.dat'
__specDataDelimiter         = '\t'

# file path (and name) to the IRF data:

__filePathRefOrIRFSpec      = 'testData/ref_10ps.dat'
__refDataDelimiter          = '\t'

# define the number of rows to be skipped during the import of the data (e.g. for ignoring the header entries):

__skipRows                  = 5;

# fixed mono-decay component in units of picoseconds [ps] (1/lambda = tau):

# Note: set to values below 1E-6 if you are providing numerical IRF data as input otherwise the decay rate in [ps]: 

__tau_monoDecaySpec_in_ps   = 182.  # [ps]

# used to simulate the IRF in case of '__demoMode' == True:

__t_zero                    = 2000             # channel number 
__irf_fwhm                  = [270.04,498.63]  # [ps]
__irf_intensity             = [0.9382,0.0618]  # [ps]
__irf_t0                    = [0.,6.6]         # [ps]

# grid of characteristic lifetimes with equally distributed grid points defining the resulting intensity spectrum to be expected as output:

__gridTau_start             = 10.0   # [ps]
__gridTau_stop              = 3000.0 # [ps]
__gridPoints                = 100    # 10 ... 100 Note: this value is internally limited by CONTIN

# channel/bin resolution [ps]:

__channelResolutionInPs     = 10. # >= 10 ... Note: this value is internally limited by CONTIN. If lower, increase '__binFactor' to fit into this range
__binFactor                 = 2   # Note: number of channels is internally limited by CONTIN to <= 4000, so adjust the '__binFactor' in order to fit the given number of channels into this range

# background estimation/calculation region:

__bkgrd_startIndex          = 6500;
__bkgrd_count               = 900; # number of channels with respect to the 'startIndex''
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
<b>pyDCONTINPALS v1.03</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4630108.svg)](https://doi.org/10.5281/zenodo.4630108)<br>
<b>pyDCONTINPALS v1.02</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4630108.svg)](https://doi.org/10.5281/zenodo.4630108)<br>
<b>pyDCONTINPALS v1.01</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4452238.svg)](https://doi.org/10.5281/zenodo.4452238)<br>
<b>pyDCONTINPALS v1.0</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3665475.svg)](https://doi.org/10.5281/zenodo.3665475)<br>
 
 # License of (py)DCONTINPALS (GNU General Public License) 
 Copyright (c) 2020-2022 Dr. Danny Petschke (danny.petschke@uni-wuerzburg.de) All rights reserved.<br>

<p align="justify">This program is free software: you can redistribute it and/or modify<br>
it under the terms of the GNU General Public License as published by<br>
the Free Software Foundation, either version 3 of the License, or<br>
(at your option) any later version.<br><br>

This program is distributed in the hope that it will be useful,<br>
but WITHOUT ANY WARRANTY; without even the implied warranty of<br>
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.<br><br></p>

For more details see [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0)
