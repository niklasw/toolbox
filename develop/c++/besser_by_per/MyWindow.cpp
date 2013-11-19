#include <QPainter>
#include <QPushButton>
#include <QWidget>
#include <QPoint>
#include <QApplication>
#include <QColor>
#include <QLabel>
#include <QTimer>
#include <QSlider>
#include <QSpinBox>
#include <QDoubleSpinBox>
#include <QRadioButton>
#include "MyWindow.h"
#include "cfd1d.h"
#include <iostream>
#include <math.h>
using namespace std;


MyWindow::MyWindow(ScalarField& f,QWidget *parent) : QWidget(parent),field(f)
{
	
	setFixedSize(400,500);
		
	QPushButton *timestepb = new QPushButton("Timestep",this);
	timestepb -> setGeometry(100,370,80,20);
	
	QPushButton *initb = new QPushButton("Init",this);
	initb -> setGeometry(10,370,80,20);

	QPushButton *runb = new QPushButton("Run",this);
	runb -> setGeometry(190,370,80,20);

	QPushButton *quitb = new QPushButton("Quit",this); 
	quitb -> setGeometry(280,370,80,20);

	QSlider *blends = new QSlider(Qt::Horizontal,this);
	blends -> setGeometry(60,345,270,20);
 	blends -> setRange(0, 100);
        blends -> setValue(100);

	QSpinBox *sizesp = new QSpinBox(this);
	sizesp -> setGeometry(60,445,270,20);
	sizesp -> setRange(3,10);
	sizesp -> setValue(7);

	QDoubleSpinBox *cflsp = new QDoubleSpinBox(this);
	cflsp -> setGeometry(60,465,270,20);
	cflsp -> setRange(0,5);
	cflsp -> setValue(0.5);
	cflsp -> setSingleStep(0.1);

	QRadioButton *efrb = new QRadioButton("Euler Forward",this);
	efrb -> setGeometry(40,400,120,20);
	efrb -> toggle();
	
	QRadioButton *rkrb = new QRadioButton("Forth Order Runge-Kutta",this);
	rkrb -> setGeometry(180,400,180,20);

	connect(initb , SIGNAL(clicked()),this, SLOT(initf()));
	connect(timestepb, SIGNAL(clicked()),this, SLOT(one_timestep()));
	connect(runb , SIGNAL(clicked()),this, SLOT(run()));
	connect(blends, SIGNAL(valueChanged(int)),this, SLOT(set_alfa(int)));
	connect(quitb, SIGNAL(clicked()),qApp, SLOT(quit()));
	connect(sizesp,SIGNAL(valueChanged(int)),this,SLOT(set_no_cells(int)));
	connect(cflsp,SIGNAL(valueChanged(double)),this,SLOT(set_cfl(double)));
	connect(efrb,SIGNAL(toggled(bool)),this,SLOT(set_time_integration(bool)));

	clf_number=0.5;
	
}

void MyWindow::paintEvent(QPaintEvent *)
{
	

	QPainter painter(this);

	painter.setBrush(Qt::SolidPattern);
	QColor c(Qt::white);
	QRectF r(10, 10, 380, 330);
	painter.fillRect(r,c);

	painter.setPen(QColor(Qt::black));
	for (int i=1;i<=field.N;i++) {
		painter.drawLine((int)(10+380*field.v[i-1]),(int)(250-150*field.q[i-1]),(int)(10+380*field.v[i]),(int)(250-150*field.q[i]));	
	}

	painter.setPen(QColor(Qt::black));
	painter.drawText(20,30,"time = " + QString::number(field.time));
	painter.drawText(30,358,"CD");
	painter.drawText(335,358,"UD");

}	

void MyWindow::one_timestep()
{	
	int n_step=1;		//Number of timesteps
	
	for (int step=0;step<n_step;step++)
	{
		field.timestep();
	} 
	
	update();
	
}

void MyWindow::set_alfa(int blending)
{
	field.alfa=blending/100.0;
}

void MyWindow::run()
{	
	int n_step=(int)(1.0/field.dt);		//Number of timesteps
	int ri=0;
	
	for (int step=0;step<n_step;step++)
	{
		field.timestep();
		ri++;
		if (ri==2) {
		repaint();
		ri=0;
		}	
	} 
	
}

void MyWindow::initf()
{
	field.init();
	update();
}

void MyWindow::set_no_cells(int size)
{
	int N=(int)(pow(2,size));
	field.no_cell(N);
	set_cfl(clf_number);
	update();

}

void MyWindow::set_cfl(double cfl)
{
	field.dt=cfl/field.N;
	clf_number=cfl;
	update();
}

void MyWindow::set_time_integration(bool ef)
{

	if(ef) {field.ti_scheme=0;}
	else {field.ti_scheme=1;}
}

