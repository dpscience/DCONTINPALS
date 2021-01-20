/****************************************************************************
**
**  Copyright (C) 2020-2021 Danny Petschke
**
**  This program is free software: you can redistribute it and/or modify
**  it under the terms of the GNU General Public License as published by
**  the Free Software Foundation, either version 3 of the License, or
**  (at your option) any later version.
**
**  This program is distributed in the hope that it will be useful,
**  but WITHOUT ANY WARRANTY; without even the implied warranty of
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
**  GNU General Public License for more details.
**
**  You should have received a copy of the GNU General Public License
**  along with this program.  If not, see http://www.gnu.org/licenses/.
**
*****************************************************************************
**
**  @author:  Danny Petschke
**  @contact: danny.petschke@uni-wuerzburg.de
**
*****************************************************************************/
#ifndef DCONTINPALS_H
#define DCONTINPALS_H

#include "dcontinpals_global.h"

#include <QFile>
#include <QTextStream>
#include <QVector>
#include <QVariant>
#include <QString>
#include <QStringBuilder>

#define EOL "\n"

#define DCONTINPALS_VERSION         1
#define DCONTINPALS_RELEASE_DATE    "11.02.2020"

class DCONTINPALSPrivateData {
public:
    DCONTINPALSPrivateData()
        : m_sumOfIntensities(0.0)  {}
    ~DCONTINPALSPrivateData() {}

    inline void clear() {
        m_x.clear();
        m_y.clear();
        m_yerr.clear();
        m_residuals.clear();
    }

    inline int size() const {
        return m_x.size();
    }

    inline int residualsSize() const {
        return m_residuals.size();
    }

    inline void append(double x, double y, double yerr) {
        m_x.append(x);
        m_y.append(y);
        m_yerr.append(yerr);
    }

    inline double sumOfIntensities(void) {
        return m_sumOfIntensities;
    }

    inline void appendResiduals(double res) {
        m_residuals.append(res);
    }

    inline void calcSumOfIntensities(void) {
        m_sumOfIntensities = 0.0;

        for (int i = 0 ; i < size() ; ++ i)
            m_sumOfIntensities += m_y.at(i);
    }

    QVector<double> m_x;
    QVector<double> m_y;
    QVector<double> m_yerr;
    QVector<double> m_residuals;

    double m_sumOfIntensities;
};

extern "C" {
    typedef struct {
        enum versionNumber : int {
            MAJOR = DCONTINPALS_VERSION
        };

        const char date[11] = DCONTINPALS_RELEASE_DATE;
    } dcpalsVersionInfo;

    enum dcpalsErrorCode : int {
        SUCCESS                                =  1,
        NO_LIFETIMEDATA                        =  0,
        NO_REFLIFETIMEDATA                     = -1,
        ZERO_BINWIDTH                          = -2,
        BADVALUE_TAUGRIDLIMITS                 = -3,
        BADVALUE_NUMBERTAUGRIDPOINTS_TOO_LOW   = -4,
        BADVALUE_NUMBERTAUGRIDPOINTS_TOO_LARGE = -5,
        BADVALUE_BACKGROUNDCHANNELS            = -6,
        DATALENGTH_TOO_HIGH                    = -7,
        DATALENGTH_TOO_SHORT                   = -8,
        BINWIDTH_TOO_SHORT                     = -9,
        NO_RESULTS                             = -10
    };

    /* accessing FORTRAN functions */
    extern void continpalsmainprogram_(void);

    bool DCONTINPALSSHARED_EXPORT prepareResults(void);

    dcpalsVersionInfo::versionNumber DCONTINPALSSHARED_EXPORT version(void);
    dcpalsErrorCode DCONTINPALSSHARED_EXPORT analyseData(int lifetimeData[],
                                                         int refLifetimeData[],
                                                         int ltDataLen,
                                                         double refMonoDecayLifetime_ps,
                                                         double binWidth_ps,
                                                         double minTauGrid_ps,
                                                         double maxTauGrid_ps,
                                                         int numberOfGridPoints,
                                                         int offsetChannelBkgrdCalc,
                                                         int numberChannelsBkgrdCalc);

    int    DCONTINPALSSHARED_EXPORT gridSize(void);
    double DCONTINPALSSHARED_EXPORT decayRateAt(int index);    // lambda [1/ns]
    double DCONTINPALSSHARED_EXPORT lifetimeAt(int index);     // tau    [ps]
    double DCONTINPALSSHARED_EXPORT intensityAt(int index);    // 0 .. 1 [a.u.]
    double DCONTINPALSSHARED_EXPORT intensityErrAt(int index); // 0 .. 1 [a.u.]

    int    DCONTINPALSSHARED_EXPORT dataSize(void);
    double DCONTINPALSSHARED_EXPORT residualsAt(int index);    // [sigma]
}

/* fort.2 */
bool createAndEditFORT2(double minTauGrid_ps,
                        double maxTauGrid_ps,
                        int numberOfGridPoints,
                        int ltDataLen,
                        double binWidth_ps);

/* fort.50 = input sample spectrum */
bool createAndEditFORT50(int lifetimeData[],
                         int offsetChannelBkgrdCalc,
                         int numberChannelsBkgrdCalc);

/* fort.51 = input reference spectrum */
bool createAndEditFORT51(int refLifetimeData[],
                         double refMonoDecayLifetime_ps,
                         int offsetChannelBkgrdCalc,
                         int numberChannelsBkgrdCalc);

/* fort.55 = sample spectrum */
bool createAndEditFORT55(int lifetimeData[],
                         int ltDataLen);

/* fort.56 = reference spectrum */
bool createAndEditFORT56(int lifetimeData[],
                         int ltDataLen);

QString formatLine(const QString& paramName,
                   double value,
                   int len,
                   int precision,
                   char format = 'f');

bool parseResultsLine(const QString line,
                      double data[3],
                      const QString& delimiter);

bool parseResultsLine2(const QString line,
                       double data[2],
                       const QString& delimiter);

void deleteAllFiles(void);

#endif // DCONTINPALS_H
