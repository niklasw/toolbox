/****************************************************************************
** Meta object code from reading C++ file 'MyWindow.h'
**
** Created: Thu Jul 5 15:14:48 2007
**      by: The Qt Meta Object Compiler version 59 (Qt 4.2.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "MyWindow.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'MyWindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 59
#error "This file was generated using the moc from 4.2.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

static const uint qt_meta_data_MyWindow[] = {

 // content:
       1,       // revision
       0,       // classname
       0,    0, // classinfo
       7,   10, // methods
       0,    0, // properties
       0,    0, // enums/sets

 // slots: signature, parameters, type, tag, flags
      10,    9,    9,    9, 0x0a,
      25,    9,    9,    9, 0x0a,
      33,    9,    9,    9, 0x0a,
      44,   39,    9,    9, 0x0a,
      63,   58,    9,    9, 0x0a,
      85,   81,    9,    9, 0x0a,
     104,  101,    9,    9, 0x0a,

       0        // eod
};

static const char qt_meta_stringdata_MyWindow[] = {
    "MyWindow\0\0one_timestep()\0initf()\0run()\0"
    "alfa\0set_alfa(int)\0size\0set_no_cells(int)\0"
    "cfl\0set_cfl(double)\0ef\0"
    "set_time_integration(bool)\0"
};

const QMetaObject MyWindow::staticMetaObject = {
    { &QWidget::staticMetaObject, qt_meta_stringdata_MyWindow,
      qt_meta_data_MyWindow, 0 }
};

const QMetaObject *MyWindow::metaObject() const
{
    return &staticMetaObject;
}

void *MyWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_MyWindow))
	return static_cast<void*>(const_cast< MyWindow*>(this));
    return QWidget::qt_metacast(_clname);
}

int MyWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: one_timestep(); break;
        case 1: initf(); break;
        case 2: run(); break;
        case 3: set_alfa((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 4: set_no_cells((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: set_cfl((*reinterpret_cast< double(*)>(_a[1]))); break;
        case 6: set_time_integration((*reinterpret_cast< bool(*)>(_a[1]))); break;
        }
        _id -= 7;
    }
    return _id;
}
