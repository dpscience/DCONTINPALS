# -*- coding: utf-8 -*-

#*************************************************************************************************
#**")
#** Copyright (c) 2020-2021 Danny Petschke. All rights reserved.
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

# NOTE: spectrum and IRF (or mono-exponential decay spectrum) data vectors require equal length!

__roi_start                 = 0
__roi_end                   = 7400

# file path (and name) to the SPECTRUM data:
__usingRefSpectrum          = True # if FALSE the '__irfXXX' related parameters are considered

__filePathSpec              = 'testData/spectrum_10ps.dat'
__specDataDelimiter         = '\t'

# file path (and name) to the IRF data:
__filePathRefOrIRFSpec      = 'testData/ref_10ps.dat'
__refDataDelimiter          = '\t'

# define the number of rows, which should be skipped during the import (e.g. for ignoring the header entries):
__skipRows                  = 5;

# fixed mono-decay component in units of picoseconds [ps] (1/lambda = tau):
# Note: set to something like 1E-6 if you provide numerical IRF data as input
__tau_monoDecaySpec_in_ps   = 182.  #[ps]

__t_zero                    = 2000
__irf_fwhm                  = [270.04,498.63]
__irf_intensity             = [0.9382,0.0618]
__irf_t0                    = [0.,6.6]

# grid of characteristic lifetimes with equally distributed grid points defining the resulting intensity spectrum
__gridTau_start             = 10.0   # [ps]
__gridTau_stop              = 3000.0 # [ps]
__gridPoints                = 100    # 10 ... 100 Note: this value is internally limited to 100 by CONTIN

# channel/bin resolution [ps]
__channelResolutionInPs     = 5.  # >= 10 ... Note: this value is internally limited by CONTIN
__binFactor                 = 1

# background estimation:
__bkgrd_startIndex          = 6500;
__bkgrd_count               = 900; # number of channels with respect to the 'startIndex'
