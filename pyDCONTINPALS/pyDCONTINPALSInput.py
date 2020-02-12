# -*- coding: utf-8 -*-

#*************************************************************************************************
#**
#** Copyright (c) 2020 Danny Petschke. All rights reserved.
#** 
#** Redistribution and use in source and binary forms, with or without modification, 
#** are permitted provided that the following conditions are met:
#**
#** 1. Redistributions of source code must retain the above copyright notice, 
#**    this list of conditions and the following disclaimer.
#**
#** 2. Redistributions in binary form must reproduce the above copyright notice, 
#**    this list of conditions and the following disclaimer in the documentation 
#**    and/or other materials provided with the distribution.
#**
#** 3. Neither the name of the copyright holder "Danny Petschke" nor the names of its  
#**    contributors may be used to endorse or promote products derived from this software  
#**    without specific prior written permission.
#**
#**
#** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
#** OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#** MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
#** COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#** EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
#** SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
#** HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
#** TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
#** EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#**
#** Contact: danny.petschke@uni-wuerzburg.de
#**
#*************************************************************************************************
__demoMode                  = True # disable if running from real data

# NOTE: spectrum and IRF (or mono-exponential decay spectrum) data vectors require equal length!

# file path (and name) to the SPECTRUM data:
__filePathSpec              = 'testData/spectrum_10ps.dat'
__specDataDelimiter         = '\t'

# file path (and name) to the IRF data:
__filePathRefOrIRFSpec      = 'testData/ref_10ps.dat'
__refDataDelimiter          = '\t'

# define the number of rows, which should be skipped during the import (e.g. for ignoring the header entries):
__skipRows                  = 5;

# fixed mono-decay component in units of picoseconds [ps] (1/lambda = tau):
# Note: set to something like 1E-6 if you provide numerical IRF data as input
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
