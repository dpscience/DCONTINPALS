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
#include "dcontinpals.h"

static DCONTINPALSPrivateData *m_results = nullptr;

dcpalsVersionInfo::versionNumber version(void) {
    return dcpalsVersionInfo::versionNumber::MAJOR;
}

dcpalsErrorCode analyseData(int lifetimeData[],
                            int refLifetimeData[],
                            int ltDataLen,
                            double refMonoDecayLifetime_ps,
                            double binWidth_ps,
                            double minTauGrid_ps,
                            double maxTauGrid_ps,
                            int numberOfGridPoints,
                            int offsetChannelBkgrdCalc,
                            int numberChannelsBkgrdCalc) {
    /* return to initial state */
    deleteAllFiles();

    if (m_results) {
        delete m_results;
        m_results = nullptr;
    }

    if (!lifetimeData) {
        return dcpalsErrorCode::NO_LIFETIMEDATA;
    }

    if (!refLifetimeData) {
        return dcpalsErrorCode::NO_REFLIFETIMEDATA;
    }

    if (ltDataLen < 10) {
        return dcpalsErrorCode::DATALENGTH_TOO_SHORT;
    }

    if (ltDataLen > 4000) // limited by CONTIN-PALS
        return dcpalsErrorCode::DATALENGTH_TOO_HIGH;

    if (binWidth_ps <= 0.0
            || qIsNull(binWidth_ps)) {
        return dcpalsErrorCode::ZERO_BINWIDTH;
    }

    if (binWidth_ps < 10.0) // limited by CONTIN-PALS
        return dcpalsErrorCode::BINWIDTH_TOO_SHORT;

    if (minTauGrid_ps <= 0.0
            || maxTauGrid_ps <= 0.0
            || maxTauGrid_ps <= minTauGrid_ps
            || qIsNull(minTauGrid_ps)
            || qIsNull(maxTauGrid_ps)) {
        return dcpalsErrorCode::BADVALUE_TAUGRIDLIMITS;
    }

    if (numberOfGridPoints <= 10) {
        return dcpalsErrorCode::BADVALUE_NUMBERTAUGRIDPOINTS_TOO_LOW;
    }

    if (numberOfGridPoints > 100) { // limited by CONTIN-PALS
        return dcpalsErrorCode::BADVALUE_NUMBERTAUGRIDPOINTS_TOO_LARGE;
    }

    if (offsetChannelBkgrdCalc + numberChannelsBkgrdCalc >= ltDataLen
            || offsetChannelBkgrdCalc >= ltDataLen
            || numberChannelsBkgrdCalc <= 1) {
        return dcpalsErrorCode::BADVALUE_BACKGROUNDCHANNELS;
    }

    /* create CONTIN-PALS compatible files */
    createAndEditFORT2(minTauGrid_ps,
                       maxTauGrid_ps,
                       numberOfGridPoints,
                       ltDataLen,
                       binWidth_ps);

    createAndEditFORT50(lifetimeData,
                        offsetChannelBkgrdCalc,
                        numberChannelsBkgrdCalc);

    createAndEditFORT51(refLifetimeData,
                        refMonoDecayLifetime_ps,
                        offsetChannelBkgrdCalc,
                        numberChannelsBkgrdCalc);

    createAndEditFORT55(lifetimeData,
                        ltDataLen);

    createAndEditFORT56(refLifetimeData,
                        ltDataLen);


    /* call CONTIN-PALS */
    continpalsmainprogram_();

    /* check for results */
    if (!prepareResults())
        return dcpalsErrorCode::NO_RESULTS;

    /* return to initial state */
    deleteAllFiles();

    return dcpalsErrorCode::SUCCESS;
}

void deleteAllFiles(void) {
    /* see CONTINPALS/CONTPALS.FOR */

    QFile::remove("FORT.2");
    QFile::remove("FORT.50");
    QFile::remove("FORT.51");
    QFile::remove("FORT.55");
    QFile::remove("FORT.56");
    QFile::remove("FORT.33");
    QFile::remove("FORT.82");
    QFile::remove("FORT.30");
    QFile::remove("FORT.11");
}

QString formatLine(const QString& paramName,
                   double value,
                   int len,
                   int precision,
                   char format) {
    QString str(paramName);

    if (!precision) {
        for (int i = 0 ; i < (7 - len - precision) ; ++ i)
            str.append(" ");
    }
    else {
        for (int i = 0 ; i < (8 - len - precision) ; ++ i)
            str.append(" ");
    }

    return str.append(QString("%1").arg(value, 0, format, precision));
}

bool createAndEditFORT2(double minTauGrid_ps,
                        double maxTauGrid_ps,
                        int numberOfGridPoints,
                        int ltDataLen,
                        double binWidth_ps) {
    QFile file("FORT.2");

    if (file.open(QIODevice::ReadWrite)) {
        QTextStream stream(&file);

        const QString endStr(EOL);

        stream << QString(" File created by DCONTINPALS") << endStr;
        stream << formatLine(" NINTT             " , 1.0, 1, 1) << endStr;

        int len = 1;

        if (numberOfGridPoints >= 10
                && numberOfGridPoints < 100)
            len = 2;
        else if (numberOfGridPoints >= 100
                 && numberOfGridPoints < 1000)
            len = 3;
        else if (numberOfGridPoints >= 1000)
            len = 4;

        stream << formatLine(" NG                " , numberOfGridPoints, len, 1) << endStr;

        len = 1;

        float val = 1.0/(maxTauGrid_ps*1E-3); /* convert to lambda value (annihilation rate) */

        if (val >= 10
                && val < 100)
            len = 2;
        else if (val >= 100
                 && val < 1000)
            len = 3;
        else if (val >= 1000)
            len = 4;

        stream << formatLine(" GMNMX     1       " , val, len, 3) << endStr;

        len = 1;

        val = 1.0/(minTauGrid_ps*1E-3); /* convert to lambda value (annihilation rate) */

        if (val >= 10
                && val < 100)
            len = 2;
        else if (val >= 100
                 && val < 1000)
            len = 3;
        else if (val >= 1000)
            len = 4;

        stream << formatLine(" GMNMX     2       " , val, len, 3) << endStr;
        stream << formatLine(" RUSER    30       " , binWidth_ps*1E-3, 1, 3) << endStr;
        stream << formatLine(" IQUAD             " , 3.0, 1, 1) << endStr;
        stream << formatLine(" IGRID             " , 2.0, 1, 1) << endStr;
        stream << formatLine(" NLINF             " , 2.0, 1, 1) << endStr;
        stream << formatLine(" NONNEG            " , 1.0, 1, 1) << endStr;
        stream << formatLine(" DOUSIN            " , 1.0, 1, 1) << endStr;
        stream << formatLine(" IUSER    10       " , 6.0, 1, 1) << endStr;
        stream << formatLine(" IUSER     2       " , 1.0, 1, 1) << endStr;
        stream << formatLine(" NEQ               " , 2.0, 1, 1) << endStr;
        stream << formatLine(" IWT               " , 2.0, 1, 1) << endStr;
        stream << formatLine(" NERFIT            " , 10.0, 2, 1) << endStr;
        stream << formatLine(" NORDER            " , 2.0, 1, 1) << endStr;
        stream << formatLine(" NENDZ     1       " , 1.0, 1, 1) << endStr;
        stream << formatLine(" NENDZ     2       " , 1.0, 1, 1) << endStr;
        stream << formatLine(" NQPROG    1       " , 5.0, 1, 1) << endStr;
        stream << formatLine(" NQPROG    2       " , 15.0, 2, 1) << endStr;
        stream << formatLine(" MOMNMX    1       " , -2.0, 2, 1) << endStr;
        stream << formatLine(" MOMNMX    2       " , 2.0, 1, 1) << endStr;
        stream << formatLine(" MIOERR            " , 5.0, 1, 1) << endStr;
        stream << formatLine(" DOUSNQ            " , -1.0, 2, 1) << endStr;
        stream << formatLine(" MPKMOM            " , 10.0, 2, 1) << endStr;
        stream << formatLine(" IUNIT             " , -3.0, 2, 1) << endStr;
        stream << formatLine(" NEWPG1            " , 1.0, 1, 1) << endStr;
        stream << formatLine(" LINEPG            " , 52.0, 2, 1) << endStr;
        stream << formatLine(" IPLRES    1       " , 0.0, 1, 1) << endStr;
        stream << formatLine(" IPLRES    2       " , 2.0, 1, 1) << endStr;
        stream << formatLine(" IPLFIT    1       " , 0.0, 1, 1) << endStr;
        stream << formatLine(" IPLFIT    2       " , 2.0, 1, 1) << endStr;
        stream << formatLine(" IPRINT    1       " , 2.0, 1, 1) << endStr;
        stream << formatLine(" IPRINT    2       " , 3.0, 1, 1) << endStr;
        stream << QString(" IFORMY") << endStr;
        stream << QString(" (8X,8F7.0)") << endStr;
        stream << QString(" END") << endStr;

        QString chnStr(" NSTEND");

        len = 1;
        if (ltDataLen >= 10
                && ltDataLen < 100)
            len = 2;
        else if (ltDataLen >= 100
                && ltDataLen < 1000)
            len = 3;
        else if (ltDataLen >= 1000
                && ltDataLen < 10000)
            len = 4;
        else if (ltDataLen >= 10000
                && ltDataLen < 100000)
            len = 5;

        if (len == 1)
            chnStr.append("    ").append(QVariant(ltDataLen).toString()).append("        1.00E+00");
        else if (len == 2)
            chnStr.append("   ").append(QVariant(ltDataLen).toString()).append("        1.00E+00");
        else if (len == 3)
            chnStr.append("  ").append(QVariant(ltDataLen).toString()).append("        1.00E+00");
        else if (len == 4)
            chnStr.append(" ").append(QVariant(ltDataLen).toString()).append("        1.00E+00");
        else if (len == 5)
            chnStr.append("").append(QVariant(ltDataLen).toString()).append("        1.00E+00");

        stream << chnStr << endStr;

        file.close();
    }
    else
        return false;

    return true;
}

bool createAndEditFORT50(int lifetimeData[],
                         int offsetChannelBkgrdCalc,
                         int numberChannelsBkgrdCalc) {
    double bkgrd = 0.0;
    for (int i = offsetChannelBkgrdCalc ; i < (offsetChannelBkgrdCalc + numberChannelsBkgrdCalc) ; ++ i)
        bkgrd += lifetimeData[i];

    bkgrd /= (double)numberChannelsBkgrdCalc;

    const int intBkgrd = (int)bkgrd;

    int len = 1;
    if (intBkgrd >= 10
            && intBkgrd < 100)
        len = 2;
    else if (intBkgrd >= 100
            && intBkgrd < 1000)
        len = 3;
    else if (intBkgrd >= 1000
            && intBkgrd < 10000)
        len = 4;
    else if (intBkgrd >= 10000
            && intBkgrd < 100000)
        len = 5;

    QFile file("FORT.50");

    if (file.open(QIODevice::ReadWrite)) {
        QTextStream stream(&file);

        const QString endStr(EOL);

        stream << QString(" IUSER    43   0.000000E+01") << endStr;
        stream << QString(" RUSER    54   0.500000E+01") << endStr;
        stream << QString(" RUSER    64   0.400000E+01") << endStr;
        stream << QString(" RUSER    55   0.500000E+01") << endStr;
        stream << QString(" RUSER    65   0.400000E+01") << endStr;
        stream << QString(" RUSER    56   0.500000E+01") << endStr;
        stream << QString(" RUSER    66   0.200000E+01") << endStr;
        stream << formatLine(" RUSER    58   ", bkgrd, len + 1, 6, 'E') << endStr;
        stream << QString(" END           0.000000E+00") << endStr;

        file.close();
    }
    else
        return false;

    return true;
}

bool createAndEditFORT51(int refLifetimeData[],
                         double refMonoDecayLifetime_ps,
                         int offsetChannelBkgrdCalc,
                         int numberChannelsBkgrdCalc) {
    double bkgrd = 0.0;
    for (int i = offsetChannelBkgrdCalc ; i < (offsetChannelBkgrdCalc + numberChannelsBkgrdCalc) ; ++ i)
        bkgrd += refLifetimeData[i];

    bkgrd /= (double)numberChannelsBkgrdCalc;

    const int intBkgrd = (int)bkgrd;

    int len = 1, len2 = 1;
    if (intBkgrd >= 10
            && intBkgrd < 100)
        len = 2;
    else if (intBkgrd >= 100
            && intBkgrd < 1000)
        len = 3;
    else if (intBkgrd >= 1000
            && intBkgrd < 10000)
        len = 4;
    else if (intBkgrd >= 10000
            && intBkgrd < 100000)
        len = 5;

    double val = 1.0/1E-12;

    if (!qIsNull(refMonoDecayLifetime_ps))
        val = 1.0/(refMonoDecayLifetime_ps*1E-3); /* convert to lambda value (annihilation rate) */

    const int intVal = (int)val;

    if (intVal >= 10
            && intVal < 100)
        len2 = 2;
    else if (intVal >= 100
            && intVal < 1000)
        len2 = 3;
    else if (intVal >= 1000
            && intVal < 10000)
        len2 = 4;
    else if (intVal >= 10000
            && intVal < 100000)
        len2 = 5;
    else if (intVal >= 100000
            && intVal < 1000000)
        len2 = 6;

    QFile file("FORT.51");

    if (file.open(QIODevice::ReadWrite)) {
        QTextStream stream(&file);

        const QString endStr(EOL);

        stream << formatLine(" RUSER    35   ", val, len2 + 1, 6, 'E') << endStr;
        stream << QString(" IUSER    40   0.000000E+01") << endStr;
        stream << QString(" RUSER    51   0.500000E+01") << endStr;
        stream << QString(" RUSER    61   0.400000E+01") << endStr;
        stream << QString(" RUSER    52   0.500000E+01") << endStr;
        stream << QString(" RUSER    62   0.400000E+01") << endStr;
        stream << QString(" RUSER    53   0.500000E+01") << endStr;
        stream << QString(" RUSER    63   0.200000E+01") << endStr;
        stream << formatLine(" RUSER    59   ", bkgrd, len + 1, 6, 'E') << endStr;
        stream << QString(" END           0.000000E+00") << endStr;

        file.close();
    }
    else
        return false;

    return true;
}

bool createAndEditFORT55(int lifetimeData[],
                         int ltDataLen) {
    QFile file("FORT.55");

    if (file.open(QIODevice::ReadWrite)) {
        QTextStream stream(&file);

        const QString endStr(EOL);

        stream << QString("sample lifetime spectrum/number of channels (%1)").arg(ltDataLen) << endStr;

        for (int i = 0 ; i < ltDataLen ; i += 8) {
            int bin = 1;
            if (i >= 10
                    && i < 100)
                bin = 2;
            else if (i >= 100
                    && i < 1000)
                bin = 3;
            else if (i >= 1000
                    && i < 10000)
                bin = 4;
            else if (i >= 10000
                    && i < 100000)
                bin = 5;
            else if (i >= 100000
                    && i < 1000000)
                bin = 6;
            else if (i >= 1000000
                    && i < 10000000)
                bin = 7;

            QString line(formatLine(" ", i, bin, 0, 'f'));

            QString _line("");
            for (int ii = 0 ; ii < 8 && (i + ii) < ltDataLen ; ++ ii) {
                const int intVal = lifetimeData[i+ii];

                int len = 1;
                if (intVal >= 10
                        && intVal < 100)
                    len = 2;
                else if (intVal >= 100
                        && intVal < 1000)
                    len = 3;
                else if (intVal >= 1000
                        && intVal < 10000)
                    len = 4;
                else if (intVal >= 10000
                        && intVal < 100000)
                    len = 5;
                else if (intVal >= 100000
                        && intVal < 1000000)
                    len = 6;
                else if (intVal >= 1000000
                        && intVal < 10000000)
                    len = 7;

                _line.append(formatLine("", intVal, len, 0, 'f'));
            }

            stream << line.append(_line) << endStr;
        }

        file.close();
    }
    else
        return false;

    return true;
}

bool createAndEditFORT56(int lifetimeData[],
                         int ltDataLen) {
    QFile file("FORT.56");

    if (file.open(QIODevice::ReadWrite)) {
        QTextStream stream(&file);

        const QString endStr(EOL);

        stream << QString("reference lifetime spectrum/number of channels (%1)").arg(ltDataLen) << endStr;

        for (int i = 0 ; i < ltDataLen ; i += 8) {
            int bin = 1;
            if (i >= 10
                    && i < 100)
                bin = 2;
            else if (i >= 100
                    && i < 1000)
                bin = 3;
            else if (i >= 1000
                    && i < 10000)
                bin = 4;
            else if (i >= 10000
                    && i < 100000)
                bin = 5;
            else if (i >= 100000
                    && i < 1000000)
                bin = 6;
            else if (i >= 1000000
                    && i < 10000000)
                bin = 7;

            QString line(formatLine(" ", i, bin, 0, 'f'));

            QString _line("");
            for (int ii = 0 ; ii < 8 && (i + ii) < ltDataLen ; ++ ii) {
                const int intVal = lifetimeData[i+ii];

                int len = 1;
                if (intVal >= 10
                        && intVal < 100)
                    len = 2;
                else if (intVal >= 100
                        && intVal < 1000)
                    len = 3;
                else if (intVal >= 1000
                        && intVal < 10000)
                    len = 4;
                else if (intVal >= 10000
                        && intVal < 100000)
                    len = 5;
                else if (intVal >= 100000
                        && intVal < 1000000)
                    len = 6;
                else if (intVal >= 1000000
                        && intVal < 10000000)
                    len = 7;

                _line.append(formatLine("", intVal, len, 0, 'f'));
            }

            stream << line.append(_line) << endStr;
        }

        file.close();
    }
    else
        return false;

    return true;
}

bool prepareResults(void) {
    if (m_results) {
        m_results->clear();

        delete m_results;
        m_results = nullptr;
    }

    m_results = new DCONTINPALSPrivateData();

    QFile file("FORT.82");

    if (!file.exists())
        return false;

    if (file.open(QIODevice::ReadOnly)) {
        QTextStream stream(&file);

        while (!stream.atEnd()) {
            const QString line = stream.readLine();

            double data[3];

            if (parseResultsLine(line, data, " "))
                m_results->append(data[0], data[1], data[2]);
        }

        file.close();
    }
    else
        return false;

    m_results->calcSumOfIntensities();

    QFile file2("FORT.11");

    if (file2.open(QIODevice::ReadOnly)) {
        QTextStream stream(&file2);

        while (!stream.atEnd()) {
            const QString line = stream.readLine();

            double data[2];

            if (parseResultsLine2(line, data, " "))
                m_results->appendResiduals(data[1]);
        }

        file2.close();
    }
    else
        return false;

    return true;
}

bool parseResultsLine(const QString line,
                      double data[],
                      const QString &delimiter) {
    if (line.isEmpty())
        return false;

    if (!data)
        return false;

    if (delimiter.isEmpty())
        return false;

    const QStringList list = line.split(delimiter, QString::SkipEmptyParts);

    if (list.size() < 2)
        return false;

    QVector<double> dataVec;

    for (QString str : list) {
        if (str.isEmpty())
            continue;

        bool ok = false;
        const double val = QVariant(str).toDouble(&ok);

        if (ok) {
            dataVec.append(val);
        }
    }

    if (dataVec.size() != 3)
        return false;

    data[0] = dataVec.at(0); // decay rate
    data[1] = dataVec.at(1); // intensity
    data[2] = dataVec.at(2); // err intensity

    return true;
}

bool parseResultsLine2(const QString line,
                       double data[],
                       const QString &delimiter) {
    if (line.isEmpty())
        return false;

    if (!data)
        return false;

    if (delimiter.isEmpty())
        return false;

    const QStringList list = line.split(delimiter, QString::SkipEmptyParts);

    if (list.size() < 2)
        return false;

    QVector<double> dataVec;

    for (QString str : list) {
        if (str.isEmpty())
            continue;

        bool ok = false;
        const double val = QVariant(str).toDouble(&ok);

        if (ok) {
            dataVec.append(val);
        }
    }

    if (dataVec.size() != 2)
        return false;

    data[0] = dataVec.at(0); // channel number
    data[1] = dataVec.at(1); // residuals

    return true;
}

int gridSize() {
    if (!m_results)
        return 0;

    return m_results->size();
}

int dataSize() {
    if (!m_results)
        return 0;

    return m_results->residualsSize();
}

double decayRateAt(int index) {
    if (!m_results)
        return -1.0;

    if (index < 0
            || index >= m_results->size())
        return 0.0;


    return m_results->m_x[index];
}

double lifetimeAt(int index) {
    if (!m_results)
        return -1.0;

    if (index < 0
            || index >= m_results->size())
        return 0.0;

    if (qIsNull(m_results->m_x[index]))
        return 0.0;

    return 1.0/(m_results->m_x[index]*1E-3);
}

double intensityAt(int index) {
    if (!m_results)
        return -1.0;

    if (index < 0
            || index >= m_results->size())
        return 0.0;

    return m_results->m_y[index]/m_results->sumOfIntensities();
}

double intensityErrAt(int index) {
    if (!m_results)
        return -1.0;

    if (index < 0
            || index >= m_results->size())
        return 0.0;

    return m_results->m_yerr[index]/m_results->sumOfIntensities();
}

double residualsAt(int index) {
    if (!m_results)
        return 0.0;

    if (index < 0
            || index >= m_results->residualsSize())
        return 0.0;

    return m_results->m_residuals[index];
}
