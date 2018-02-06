#ifndef QTPLOT
#define QTPLOT

#include <iostream>
#include <vector>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>

QT_CHARTS_USE_NAMESPACE


unique_ptr<QChart> makeChart(const std::vector<double>& X, const std::vector<double>& Y)
{
    unique_ptr<QLineSeries> series(new QLineSeries());

    for(int i=0; i< X.size(); i++)
    {
        double x = X[i];
        double y = Y[i];
        series->append(x,y);
    }

    unique_ptr<QChart> chart(new QChart());
    chart->legend()->hide();
    chart->addSeries(series.get());
    chart->createDefaultAxes();
    chart->setTitle("Simple line chart example");
    return chart;
}

template<typename TX, typename TY>
void
doPlot(int argc, char *argv[], const std::vector<TX>& X, const std::vector<TY>& Y)
{
    vector<double> yy(Y.begin(), Y.end());
    vector<double> xx(X.begin(), X.end());

    /*
    unique_ptr<QChart> chart = makeChart(xx,yy);

    unique_ptr<QChartView> chartView(new QChartView(chart.get()));
    chartView->setRenderHint(QPainter::Antialiasing);

    unique_ptr<QMainWindow>  window(new QMainWindow());
    window->setCentralWidget(chartView.get());
    window->resize(800, 600);
    window->show();

    unique_ptr<QApplication> aPtr(new QApplication(argc,argv));

    aPtr->exec();
    */

    return;
};

#endif
