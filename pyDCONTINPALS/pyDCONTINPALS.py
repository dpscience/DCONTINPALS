# -*- coding: utf-8 -*-

VERSION_HANDSHAKE = 1 # v1.0x

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

import ctypes
from ctypes import cdll
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import pyDCONTINPALSSpecSimulator as specSimulator
import pyDCONTINPALSInput as userInput

def __information__():
    print("#********************* pyDCONTINPALS 1.01 (20.01.2021) *********************")
    print("#**")
    print("#** Copyright (C) 2020-2021 Danny Petschke")
    print("#**")
    print("#** Contact: danny.petschke@uni-wuerzburg.de")
    print("#**")
    print("#***************************************************************************\n")

def __licence__():
    print("#*************************************************************************************************")
    print("#**")
    print("#** Copyright (c) 2020-2021 Danny Petschke. All rights reserved.")
    print("#**")
    print("#** This program is free software: you can redistribute it and/or modify") 
    print("#** it under the terms of the GNU General Public License as published by")
    print("#** the Free Software Foundation, either version 3 of the License, or")
    print("#** (at your option) any later version.")
    print("#**")
    print("#** This program is distributed in the hope that it will be useful,") 
    print("#** but WITHOUT ANY WARRANTY; without even the implied warranty of") 
    print("#** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the")
    print("#** GNU General Public License for more details.")  
    print("#**")
    print("#** You should have received a copy of the GNU General Public License")  
    print("#** along with this program. If not, see http://www.gnu.org/licenses/.")
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