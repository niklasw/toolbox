#ifndef QTPLOT
#define QTPLOT

#include <iostream>
#include <vector>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>

QT_CHARTS_USE_NAMESPACE

void doPlot
(
    int argc,
    char *argv[],
    const std::vector<double>& X,
    const std::vector<double>& Y
);

#endif
