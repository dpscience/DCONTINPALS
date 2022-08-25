# -*- coding: utf-8 -*-

#*************************************************************************************************
#**")
#** Copyright (c) 2020-2022 Dr. Danny Petschke. All rights reserved.
#**")
#** This program is free software: you can redistribute it and/or modify
#** it under the terms of the GNU General Public License as published by
#** the Free Software Foundation, either version 3 of the License, or
#** (at your option) any later version.
#**
#** This program is distributed in the hope that it will be useful,
#** but WITHOUT ANY WARRANTY; without even the implied warranty of
#** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#** GNU General Public License for more details.
#**")
#** You should have received a copy of the GNU General Public License
#** along with this program. If not, see http://www.gnu.org/licenses/.
#**
#** Contact: danny.petschke@uni-wuerzburg.de
#**
#*************************************************************************************************

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
__bkgrd_count               = 900; # number of channels with respect to the 'startIndex'
