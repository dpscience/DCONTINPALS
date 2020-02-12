# -*- coding: utf-8 -*-

VERSION_HANDSHAKE = 1 # v1.0

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

import ctypes
from ctypes import cdll
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import pyDCONTINPALSSpecSimulator as specSimulator
import pyDCONTINPALSInput as userInput

def __information__():
    print("#****************** pyDCONTINPALS 1.0 (11.02.2020) *******************")
    print("#**")
    print("#** Copyright (C) 2020 Danny Petschke")
    print("#**")
    print("#** Contact: danny.petschke@uni-wuerzburg.de")
    print("#**")
    print("#***************************************************************************\n")

def __licence__():
    print("#*************************************************************************************************")
    print("#**")
    print("#** Copyright (c) 2020 Danny Petschke. All rights reserved.")
    print("#**")
    print("#** Redistribution and use in source and binary forms, with or without modification,") 
    print("#** are permitted provided that the following conditions are met:")
    print("#**")
    print("#** 1. Redistributions of source code must retain the above copyright notice,")
    print("#**    this list of conditions and the following disclaimer.")
    print("#**")
    print("#** 2. Redistributions in binary form must reproduce the above copyright notice,") 
    print("#**    this list of conditions and the following disclaimer in the documentation") 
    print("#**    and/or other materials provided with the distribution.")
    print("#**")
    print("#** 3. Neither the name of the copyright holder ""Danny Petschke"" nor the names of its")  
    print("#**    contributors may be used to endorse or promote products derived from this software")  
    print("#**    without specific prior written permission.")
    print("#**")
    print("#**")
    print("#** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ""AS IS"" AND ANY EXPRESS") 
    print("#** OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF") 
    print("#** MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE") 
    print("#** COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,") 
    print("#** EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF") 
    print("#** SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)") 
    print("#** HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR") 
    print("#** TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,") 
    print("#** EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.")
    print("#**")
    print("#** Contact: danny.petschke@uni-wuerzburg.de")
    print("#**")
    print("#*************************************************************************************************")

if __name__ == '__main__':
    __information__()
    
    # (1) check for the currently required version
    __dllPtr = cdll.LoadLibrary('dcontinpals.dll')
    
    if not (__dllPtr.version() == VERSION_HANDSHAKE):
        print("version misfit: dcontinpals.dll (v{0}) vs. pyDCONTINPALS (v{1})".format(__dllPtr.version(), VERSION_HANDSHAKE))
        exit();
        
    monoDecayTau   = userInput.__tau_monoDecaySpec_in_ps
    binWidth_in_ps = userInput.__channelResolutionInPs
    tauGrid_in_ps  = [userInput.__gridTau_start, userInput.__gridTau_stop]
    gridPoints     = userInput.__gridPoints
        
    # running demo mode ?
    if userInput.__demoMode:
        numberOfBins = userInput.__bkgrd_startIndex + userInput.__bkgrd_count + 10 # set to the maximum for demonstration purposes
        
        charactLifetimes_in_ps  = [160.0, 400.0, 2000.0]
        contributionOfLifetimes = [0.90,  0.095, 0.005]
        
        specdata_sample = specSimulator.generateCompleteLTSpectrum(numberOfComponents=len(charactLifetimes_in_ps),
                                                                    binWidth_in_ps=binWidth_in_ps, 
                                                                    integralCounts=5000000, 
                                                                    constBkgrdCounts=5, 
                                                                    numberOfBins=numberOfBins, 
                                                                    charactLifetimes_in_ps=charactLifetimes_in_ps, 
                                                                    contributionOfLifetimes=contributionOfLifetimes,
                                                                    irf_tZero_in_ps=3500.0,
                                                                    irf_fwhm_in_ps=230.0,
                                                                    noise=True,
                                                                    noiseLevel=1.0)
        
        specdata_ref = specSimulator.generateCompleteLTSpectrum(numberOfComponents=1,
                                                                    binWidth_in_ps=binWidth_in_ps, 
                                                                    integralCounts=5000000, 
                                                                    constBkgrdCounts=5, 
                                                                    numberOfBins=numberOfBins, 
                                                                    charactLifetimes_in_ps=[monoDecayTau], 
                                                                    contributionOfLifetimes=[1.0],
                                                                    irf_tZero_in_ps=3500.0,
                                                                    irf_fwhm_in_ps=230.0,
                                                                    noise=True,
                                                                    noiseLevel=1.0)
    else:
        __ ,specdata_sample = np.loadtxt(userInput.__filePathSpec, delimiter=userInput.__specDataDelimiter, skiprows=userInput.__skipRows, unpack=True, dtype='float');
        __ ,specdata_ref    = np.loadtxt(userInput.__filePathRefOrIRFSpec, delimiter=userInput.__refDataDelimiter, skiprows=userInput.__skipRows, unpack=True, dtype='float');

        numberOfBins = len(specdata_sample)
        
    # catch general limitations given by CONTIN-PALS
    assert numberOfBins <= 4000 and numberOfBins >= 10 
    assert gridPoints >= 10 and gridPoints <= 100
    assert binWidth_in_ps >= 10.0
    
    if monoDecayTau == 0.0:
        monoDecayTau = 1E-6

    # show the data
    fig, ax = plt.subplots()
    plt.semilogy(specdata_sample, 'bo', specdata_ref, 'ro')
    ax.set_ylabel('counts [a.u.]')
    ax.set_xlabel('channel [a.u.]')
    plt.show()
    
    specSamp = (ctypes.c_int*numberOfBins)()
    specRef  = (ctypes.c_int*numberOfBins)()
    
    for i in range(numberOfBins):
        specSamp[i] = int(specdata_sample[i])
        specRef[i]  = int(specdata_ref[i])
    
    program          = __dllPtr.analyseData
    program.restype = ctypes.c_int
    
    # run CONTIN-PALS
    result = program(specSamp,
                     specRef,
                     ctypes.c_int(numberOfBins),
                     ctypes.c_double(monoDecayTau),
                     ctypes.c_double(binWidth_in_ps),
                     ctypes.c_double(tauGrid_in_ps[0]),
                     ctypes.c_double(tauGrid_in_ps[1]),
                     ctypes.c_int(gridPoints),
                     ctypes.c_int(userInput.__bkgrd_startIndex),
                     ctypes.c_int(userInput.__bkgrd_count))
    
    if not result == 1:
        if result == 0:
            print("no lifetime data available")
        elif result == -1:
            print("no reference data (IRF or mono-decay sepctrum) available")
        elif result == -2:
            print("zero (= 0.0 ps) binning detected")
        elif result == -3:
            print("grid limits are badly set")
        elif result == -4:
            print("number of grid points too low (must be >= 10)")
        elif result == -5:
            print("number of grid points too high (must be <= 1000)")
        elif result == -6:
            print("indices for background estimation are badly set")
        elif result == -7:
            print("data vector too long (must be <= 4000)")
        elif result == -8:
            print("data vector too short (must be >= 10)")
        elif result == -9:
            print("binning too short (must be >= 10 ps)")
        elif result == -10:
            print("no results available")
            
        #exit()
        
    m_x    = __dllPtr.lifetimeAt
    m_y    = __dllPtr.intensityAt
    m_yerr = __dllPtr.intensityErrAt
    m_res  = __dllPtr.residualsAt
    
    m_x.restype    = ctypes.c_double 
    m_y.restype    = ctypes.c_double 
    m_yerr.restype = ctypes.c_double 
    m_res.restype  = ctypes.c_double 
        
    x     = np.zeros(gridPoints)
    y     = np.zeros(gridPoints)
    yerr  = np.zeros(gridPoints)
    
    res   = np.zeros(numberOfBins)
    
    # visualize results
    for i in range(0, gridPoints):
        x[i]    = m_x(ctypes.c_int(i))
        y[i]    = m_y(ctypes.c_int(i))
        yerr[i] = m_yerr(ctypes.c_int(i))
        
    for i in range(0, numberOfBins):
        res[i]  = m_res(ctypes.c_int(i))
        
    fig, ax = plt.subplots()
    plt.errorbar(x, y, yerr=yerr)
    
    # running demo mode ?
    if userInput.__demoMode:
        for xc in charactLifetimes_in_ps:
            plt.axvline(x=xc, color='k', linestyle='--')
        
    ax.set_ylabel('intensity [a.u.]')
    ax.set_xlabel('characteristic lifetimes [ps]')
    plt.show()
    
    fig, ax = plt.subplots()
    plt.plot(res, 'ro')
    
    hlines = [-2, 0 , 2]    
    for yc in hlines:
        plt.axhline(y=yc, color='k', linestyle='--')
        
    ax.set_ylabel('confidence level [sigma]')
    ax.set_xlabel('channel [a.u.]')
    plt.show()