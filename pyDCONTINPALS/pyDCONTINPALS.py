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
from scipy.optimize import curve_fit
from scipy import interpolate

import pyDCONTINPALSSpecSimulator as specSimulator
import pyDCONTINPALSInput as userInput

def __information__():
    print("#********************* pyDCONTINPALS 1.02 (16.03.2021) *********************")
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

def gaussian(x=[],amplitude=1.,loc=0.,scale=1.):
    return amplitude*np.exp(-0.5*((x-loc)/scale)**2)
    
def detectPeaks(x=[],y=[]):
    peak_list = []
    peak_list_y = []
    
    der_1st = []
    for i in range(0,len(y)-1):
        der_1st.append((y[i+1]-y[i])/(x[i+1]-x[i]))
        
    #plt.plot(der_1st,'ro')
    #plt.show()
    
    for i in range(0,len(der_1st)-1):
        p1=der_1st[i]   
        p2=der_1st[i+1]
        
        if np.abs(p1-p2)<=1e-5:
            continue
            
        if (p1 > 0 and p2 < 0) or (p2 > 0 and p1 < 0):
            peak_list.append(x[i+1])
            peak_list_y.append(y[i+1])
                
    return peak_list,peak_list_y
    
def multiPeakFit(x=[],y=[]):
    peak_list_x,peak_list_y = detectPeaks(x,y)
    
    results = []
    results_uncertainties = []
    results_curve = []
    results_area = []
    
    for i in range(0,len(peak_list_x)):
        init_vals = [peak_list_y[i],peak_list_x[i],50.]
        
        best_vals,covar = curve_fit(gaussian,x,y,p0=init_vals)
        
        results.append(best_vals)
        results_uncertainties.append(np.sqrt(np.diag(covar)))
        results_curve.append(gaussian(x,amplitude=best_vals[0],loc=best_vals[1],scale=best_vals[2]))
        results_area.append(sum(gaussian(x,amplitude=best_vals[0],loc=best_vals[1],scale=best_vals[2])))
            
    return results,results_uncertainties,results_curve,results_area

if __name__ == '__main__':
    __information__()
    
    # (1) check for the currently required version
    __dllPtr = cdll.LoadLibrary('dcontinpals.dll')
    
    if not (__dllPtr.version() == VERSION_HANDSHAKE):
        print("version misfit: dcontinpals.dll (v{0}) vs. pyDCONTINPALS (v{1})".format(__dllPtr.version(), VERSION_HANDSHAKE))
        exit();
        
    monoDecayTau   = userInput.__tau_monoDecaySpec_in_ps
    binWidth_in_ps = userInput.__channelResolutionInPs
    tauGrid_in_ps  = [userInput.__gridTau_start,userInput.__gridTau_stop]
    gridPoints     = userInput.__gridPoints
    binFac         = userInput.__binFactor
        
    # running demo mode ?
    if userInput.__demoMode:
        numberOfBins = userInput.__bkgrd_startIndex + userInput.__bkgrd_count + 10 # set to the maximum for demonstration purposes
        
        charactLifetimes_in_ps  = [180.0, 400.0, 1600.0]
        contributionOfLifetimes = [0.30,  0.50, 0.20]
        
        specdata_sample = specSimulator.generateCompleteLTSpectrum(numberOfComponents=len(charactLifetimes_in_ps),
                                                                    binWidth_in_ps=binWidth_in_ps, 
                                                                    integralCounts=5000000, 
                                                                    constBkgrdCounts=5, 
                                                                    numberOfBins=numberOfBins, 
                                                                    charactLifetimes_in_ps=charactLifetimes_in_ps, 
                                                                    contributionOfLifetimes=contributionOfLifetimes,
                                                                    irf_tZero_in_ps=userInput.__t_zero*userInput.__channelResolutionInPs,
                                                                    irf_fwhm_in_ps=230.0,
                                                                    noise=True,
                                                                    noiseLevel=1.0)
        
        specdata_ref = specSimulator.generateCompleteLTSpectrum(numberOfComponents=3,
                                                                    binWidth_in_ps=binWidth_in_ps, 
                                                                    integralCounts=5000000, 
                                                                    constBkgrdCounts=5, 
                                                                    numberOfBins=numberOfBins, 
                                                                    charactLifetimes_in_ps=[userInput.__tau_monoDecaySpec_in_ps], 
                                                                    contributionOfLifetimes=[1.],
                                                                    irf_tZero_in_ps=userInput.__t_zero*userInput.__channelResolutionInPs,
                                                                    irf_fwhm_in_ps=230.0,
                                                                    noise=True,
                                                                    noiseLevel=1.0)
    else:
        specdata_sample = np.loadtxt(userInput.__filePathSpec, delimiter=userInput.__specDataDelimiter, skiprows=userInput.__skipRows, unpack=True, dtype='float')
        
        if userInput.__usingRefSpectrum:
            specdata_ref = np.loadtxt(userInput.__filePathRefOrIRFSpec, delimiter=userInput.__refDataDelimiter, skiprows=userInput.__skipRows, unpack=True, dtype='float')
        else:
            specdata_ref = np.zeros(len(specdata_sample))
        
    spec_rebinned = np.zeros(int(np.ceil(len(specdata_sample)/binFac)))
    
    i_bin = 0
    sum_bins = 0.
    for i in range(0,len(specdata_sample)):
        sum_bins += specdata_sample[i]
        if not i%binFac:
            spec_rebinned[i_bin] = sum_bins
            i_bin += 1
            sum_bins = 0.
            
    specdata_sample = spec_rebinned
    
    if not userInput.__usingRefSpectrum:
        for i in range(len(specdata_ref)):
            t = (i-userInput.__t_zero)*binWidth_in_ps
            
            a = 0
            for ii in range(len(userInput.__irf_fwhm)):
                a += userInput.__irf_intensity[ii]*np.exp(-0.5*((t-userInput.__irf_t0[ii])/(userInput.__irf_fwhm[ii]/2.3548))**2)
                
            specdata_ref[i] = a
        
    irf_rebinned = np.zeros(int(np.ceil(len(specdata_ref)/binFac)))
    
    i_bin = 0
    sum_bins = 0.
    for i in range(0,len(specdata_ref)):
        sum_bins += specdata_ref[i]
        if not i%binFac:
            irf_rebinned[i_bin] = sum_bins
            i_bin += 1
            sum_bins = 0.
            
    specdata_ref = irf_rebinned
    
    # adjust values to rebinned data ...
    binWidth_in_ps *= binFac
    
    roi_start = int(np.ceil(userInput.__roi_start/binFac))
    roi_end   = int(np.ceil(userInput.__roi_end/binFac))
    
    bkgrd_startIndex = int(np.ceil(userInput.__bkgrd_startIndex/binFac))
    bkgrd_count      = int(np.ceil(userInput.__bkgrd_count/binFac))
    
    bkgrd_startIndex -= roi_start+1
    
    t_zero_chn = int(np.ceil(userInput.__t_zero/binFac))
    
    spec_data_roi = specdata_sample[roi_start:roi_end]
    irf_data_roi  = specdata_ref[roi_start:roi_end]
    
    numberOfBins = len(spec_data_roi)
        
    # catch general limitations given by CONTIN-PALS
    assert numberOfBins <= 4000 and numberOfBins >= 10 
    assert gridPoints >= 10 and gridPoints <= 100
    assert binWidth_in_ps >= 10.0
    
    if not userInput.__usingRefSpectrum:
        monoDecayTau = 1E-6

    # show the data
    fig, ax = plt.subplots()
    
    if userInput.__usingRefSpectrum:
        plt.semilogy(spec_data_roi/sum(spec_data_roi), 'bo', irf_data_roi/sum(irf_data_roi), 'r-')
    else:
        plt.semilogy(spec_data_roi/sum(spec_data_roi), 'bo')
        
    ax.set_ylabel('area normalized counts [a.u.]')
    ax.set_xlabel('channels [{} ps]'.format(binWidth_in_ps))
    plt.show()
    
    specSamp = (ctypes.c_int*numberOfBins)()
    specRef  = (ctypes.c_int*numberOfBins)()
    
    for i in range(numberOfBins):
        specSamp[i] = int(spec_data_roi[i])
        specRef[i]  = int(irf_data_roi[i])
    
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
                     ctypes.c_int(bkgrd_startIndex),
                     ctypes.c_int(bkgrd_count))
    
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
        
    x    = np.zeros(gridPoints)
    y    = np.zeros(gridPoints)
    yerr = np.zeros(gridPoints)
    
    res  = np.zeros(numberOfBins)
    
    # visualize results
    for i in range(0, gridPoints):
        x[i]    = m_x(ctypes.c_int(i))
        y[i]    = m_y(ctypes.c_int(i))
        yerr[i] = m_yerr(ctypes.c_int(i))
        
    # fit results to retrieve information ...
    results,uncertainties,fitData,intensities = multiPeakFit(x,y)    
    
    for i in range(0, numberOfBins):
        res[i]  = m_res(ctypes.c_int(i))
        
    fig, ax = plt.subplots()
    plt.errorbar(x,y,yerr=yerr,marker='s',mfc='red',mec='blue', ms=2, mew=4,label="CONTIN-PALS results")
    
    for i in range(0,len(fitData)):
        plt.plot(x,fitData[i],'r--',lw=1,label='Gaussian fit at {} ps'.format(results[i][1]))
        
        x_v = [results[i][1],results[i][1]]
        y_v = [0,results[i][0]]
        
        plt.plot(x_v,y_v,'r-',lw=2)
    
    # running demo mode ?
    if userInput.__demoMode:
        for xc in charactLifetimes_in_ps:
            plt.axvline(x=xc, color='k', linestyle='--')
        
    ax.set_ylabel('intensity pdf [a.u.]')
    ax.set_xlabel('characteristic lifetimes [ps]')
    plt.legend(loc='best')
    plt.show()
    
    fig, ax = plt.subplots()
    plt.plot(res,'ro',label="error normalized residuals")
    plt.legend(loc='best')
    
    hlines = [-4,-2,0,2,4]    
    for yc in hlines:
        plt.axhline(y=yc, color='k', linestyle='--')
        
    ax.set_ylabel('confidence level [sigma]')
    ax.set_xlabel('channels [{} ps]'.format(binWidth_in_ps))
    ax.set_ylim([-6,6])
    plt.show()
    
    print('')
    print('channel-width:  {} ps (= {} x {} ps)'.format(binWidth_in_ps,binFac,userInput.__channelResolutionInPs))
    print('')
    print('ROI:            [{} : {}]'.format(roi_start,roi_end))
    
    if not userInput.__usingRefSpectrum:
        print('t-zero channel: {}'.format(t_zero_chn))
        
    print('background:     [{} : {}]'.format(bkgrd_startIndex,bkgrd_startIndex+bkgrd_count))
    print('')
    
    if not userInput.__usingRefSpectrum:
        for i in range(len(userInput.__irf_fwhm)):
            print('----- fixed Gaussian IRF components ({}/{}) -----'.format(i+1,len(userInput.__irf_fwhm)))
            print('')
            print('intensity:  {} %'.format(100.*userInput.__irf_intensity[i]))
            print('t:          {} ps'.format(userInput.__irf_t0[i]))
            print('FWHM:       {} ps'.format(userInput.__irf_fwhm[i]))
        
        print('')
        
    for i in range(0,len(results)):
        print('------------ found component ({}/{}) ------------'.format(i+1,len(results)))
        print('')
        print('tau-mean:   ({} +/- {}) ps'.format(results[i][1],uncertainties[i][1]))
        print('tau-sigma:  ({} +/- {}) ps'.format(results[i][2],uncertainties[i][2]))
        print('')
        print('intensity:  {} %'.format(100.*intensities[i]/sum(intensities)))
        print('')
    
    
    
    
    
