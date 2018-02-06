#include "qtPlot.h"

QChart* makeChart(const std::vector<double>& X, const std::vector<double>& Y)
{
    QLineSeries *series = new QLineSeries();

    for(int i=0; i< X.size(); i++)
    {
        double x = X[i];
        double y = Y[i];
        series->append(x,y);
    }

    QChart *chart = new QChart();
    chart->legend()->hide();
    chart->addSeries(series);
    chart->createDefaultAxes();
    chart->setTitle("Simple line chart example");
    return chart;
}

void doPlot(int argc, char *argv[], const std::vector<double>& X, const std::vector<double>& Y)
{
    QApplication a(argc,argv);

    QChart *chart = makeChart(X,Y);

    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    QMainWindow window;
    window.setCentralWidget(chartView);
    window.resize(800, 600);
    window.show();

    a.exec();
    return;
};
