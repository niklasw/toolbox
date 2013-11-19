#include <QApplication>

#include "MyWindow.h"
#include "cfd1d.h"

int main(int argc, char *argv[])
{
	QApplication app(argc, argv);
	ScalarField s(128);
    MyWindow plot(s);	
    plot.show();
    return app.exec();
}
