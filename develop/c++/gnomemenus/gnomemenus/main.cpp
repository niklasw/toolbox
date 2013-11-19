/***************************************************************************
                          main.cpp  -  description
                             -------------------
    begin                : Tue Apr  1 00:05:03 CEST 2003
    copyright            : (C) 2003 by Niklas Wikstrom
    email                : nikwik@foi.se
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <iostream.h>
#include <stdlib.h>
#include "list.h"

int main(int argc, char *argv[])
{
  cout << "Hello, World!" << endl;
  list<int> argList(4);
  cout << argList[0];
  return EXIT_SUCCESS;
}
