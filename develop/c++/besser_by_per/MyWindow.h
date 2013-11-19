#ifndef MYWINDOW_H
#define MYWINDOW_H

#include <QWidget>
#include <QPainter>
#include "cfd1d.h"


class MyWindow : public QWidget
{
	Q_OBJECT

public:
	MyWindow(ScalarField& f,QWidget *parent=0);
	ScalarField& field;
	double clf_number;


public slots:
	void one_timestep();
	void initf();
	void run();
	void set_alfa(int alfa);
	void set_no_cells(int size);
	void set_cfl(double cfl);
	void set_time_integration(bool ef);

	

protected:
	void paintEvent(QPaintEvent *event);
};

#endif 
