/***************************************************************************
                          list.h  -  description
                             -------------------
    begin                : Tue Apr 1 2003
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

#ifndef LIST_H
#define LIST_H


/**top list class
  *@author Niklas Wikstrom
  */
template <class T>
class list {
public:
  list(int i=0)
  :len_(i) {}

  list(const list& l)
  :l_(0) {*this = l;}

  list(const T[])  
 ~list(){delete[] l_;}
  
private:
  T *l_;
  int len_;
};

#endif
