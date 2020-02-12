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

from ctypes import cdll
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from copy import deepcopy
    
# gaussian distribution function: G(mu = t_zero_in_ps, fwhm)
def generateGaussianIRF(binWidth_in_ps=5.0, 
                        numberOfIntegralCounts=5000000, 
                        constBkgrdCounts=0,
                        numberOfBins=10000,
                        tZero_in_ps=0.0,
                        fwhm_in_ps=230.0,
                        noise=True,
                        noiseLevel=1.0):
    
    # providing multiple gaussian functions
    numberOfComponents = 1
    intensitiesOfGaussian = [1.0]
    
    timeBin_in_ps = np.zeros(numberOfBins)
    counts_y      = np.zeros(numberOfBins)
    
    countsInitial = np.zeros(numberOfComponents)
    areaInitial   = np.zeros(numberOfComponents) 
    
    sumOfCounts   = 0
    
    sigma         = fwhm_in_ps/(2*np.sqrt(2*np.log(2)))

    for i in range(0, numberOfComponents):
        countsInitial[i] = numberOfIntegralCounts*intensitiesOfGaussian[i]
    
    for bin in range(0, numberOfBins - 1):
        timeBin_in_ps[bin] = (2*bin + 1)*binWidth_in_ps*0.5 
        
        for i in range(0, numberOfComponents):
            areaInitial[i] += (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((timeBin_in_ps[bin]-tZero_in_ps)/sigma)**2)
        
    for i in range(0, numberOfComponents):
        areaInitial[i] *= intensitiesOfGaussian[i]*numberOfComponents
            
    for bin in range(0, numberOfBins):
        for i in range(0, numberOfComponents):
            counts_y[bin] += (countsInitial[i]/areaInitial[i])*(1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((timeBin_in_ps[bin]-tZero_in_ps)/sigma)**2) 
            
        counts_y[bin] += float(constBkgrdCounts)
                
        if noise:
            counts_y[bin] += int(poissonNoise(counts_y[bin], noiseLevel))
            
            if counts_y[bin] < 0:
                counts_y[bin] = 0   
            
        sumOfCounts += (int)(counts_y[bin])
     
    return counts_y

# convolution of numerical data using the convolution theorem
def convolveData(a, b):
    A = np.fft.fft(a);
    B = np.fft.fft(b);
    convAB = np.real(np.fft.ifft(A*B));
    return convAB;

# poisson noise(λ) = gaussian(μ = λ, σ² = λ)
def poissonNoise(mean, noise=1.0):
    return np.random.normal(loc=0.0, scale=noise*np.sqrt(mean + 1), size=None)

# SNR estimation for transients according to Schrader and Usmar [in: Positron Annihilation Studies of Fluids, ed. S. Sharma (World Scientific, Singapore, 1988) p.215]
def retrieveSNR(data, startBin):
    snr_n = 0.0
    snr_d = 0.0
    for i in range(startBin, len(data)):
        snr_n += np.sqrt(data[i])
        snr_d += data[i]
    return snr_n/snr_d
    
# ideal lifetime spectrum: sum of N discrete exponential decays according to I*exp(-t/tau)
def generateLTSpectrum(numberOfComponents=3, 
                       binWidth_in_ps=5.0, 
                       integralCounts=5000000, 
                       constBkgrdCounts=0, 
                       numberOfBins=10000, 
                       charactLifetimes_in_ps=[160.0, 380.0, 1300.0], 
                       contributionOfLifetimes=[0.8, 0.15, 0.05],
                       noise=True,
                       noiseLevel=1.0):
    
    assert sum(contributionOfLifetimes) == 1.0
    
    timeBin_in_ps = np.zeros(numberOfBins)
    counts_y      = np.zeros(numberOfBins)
    
    integralCounts -= float(constBkgrdCounts*numberOfBins)
    
    assert integralCounts > 0
    assert numberOfBins > 0
    assert numberOfComponents >= 1
    assert binWidth_in_ps > 0.1
    assert constBkgrdCounts >= 0
    assert noiseLevel > 0.0
    assert len(charactLifetimes_in_ps) == len(contributionOfLifetimes)
    
    for i in range(0, numberOfComponents):
        assert charactLifetimes_in_ps[i] > 0.0
        
    countsInitial = np.zeros(numberOfComponents)
    areaInitial   = np.zeros(numberOfComponents) 
    
    sumOfCounts   = 0
    
    for bin in range(0, numberOfBins):
        timeBin_in_ps[bin] = float(bin)*binWidth_in_ps
              
        for i in range(0, numberOfComponents):
            areaInitial[i] += float(np.exp(-timeBin_in_ps[bin]/charactLifetimes_in_ps[i]))
        
    for i in range(0, numberOfComponents):
        countsInitial[i] = float(integralCounts)*contributionOfLifetimes[i]
           
    for bin in range(0, numberOfBins):
        for i in range(0, numberOfComponents):
            counts_y[bin] += float((countsInitial[i]/areaInitial[i]))*np.exp(-timeBin_in_ps[bin]/charactLifetimes_in_ps[i])
        
        counts_y[bin] += float(constBkgrdCounts)
                
        if noise:
            counts_y[bin] += int(poissonNoise(counts_y[bin], noiseLevel))
            
            if counts_y[bin] < 0:
                counts_y[bin] = 0
            
        sumOfCounts += (int)(counts_y[bin])

    return np.arange(0, numberOfBins, 1), counts_y, sumOfCounts


def generateCompleteLTSpectrum(numberOfComponents=3, 
                       binWidth_in_ps=5.0, 
                       integralCounts=5000000, 
                       constBkgrdCounts=0, 
                       numberOfBins=10000, 
                       charactLifetimes_in_ps=[160.0, 380.0, 1300.0], 
                       contributionOfLifetimes=[0.8, 0.15, 0.05],
                       irf_tZero_in_ps=0.0,
                       irf_fwhm_in_ps=230.0,
                       noise=True,
                       noiseLevel=1.0):
    yIRF = generateGaussianIRF(binWidth_in_ps=binWidth_in_ps, 
                        numberOfIntegralCounts=integralCounts, 
                        constBkgrdCounts=constBkgrdCounts,
                        numberOfBins=numberOfBins,
                        tZero_in_ps=irf_tZero_in_ps,
                        fwhm_in_ps=irf_fwhm_in_ps,
                        noise=False,
                        noiseLevel=1.0)

    __, ySpec, __ = generateLTSpectrum(numberOfComponents=numberOfComponents, 
                       binWidth_in_ps=binWidth_in_ps, 
                       integralCounts=integralCounts, 
                       constBkgrdCounts=constBkgrdCounts, 
                       numberOfBins=numberOfBins, 
                       charactLifetimes_in_ps=charactLifetimes_in_ps, 
                       contributionOfLifetimes=contributionOfLifetimes,
                       noise=False,
                       noiseLevel=1.0)
    
    yIRF /= sum(yIRF)
    ySpec = convolveData(ySpec, yIRF)

    if noise:
        for z in range(0, len(ySpec)):
            ySpec[z] += int(poissonNoise(ySpec[z], noiseLevel))
                
            if ySpec[z] < 0:
                ySpec[z] = 0
    
    return ySpec