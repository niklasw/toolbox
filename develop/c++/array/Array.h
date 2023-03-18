#ifndef MYARRAY_H
#define MYARRAY_H

#include <iostream>
#include <array>


template<typename T, size_t N>
class Array : public std::array<T,N>
{
    public:
        Array();

        Array(T);

        //- unary operators should belong to class
        void operator+=(const Array& p);
        void operator+=(T d);

        //- binary operators should be friends (not belong to class)
        Array operator+(const T& d);

        Array operator+(const Array& p2);

        template<typename Type, size_t S>
        friend std::ostream& operator<<(std::ostream& os, const Array<Type,S>& p);

        template<typename Type, size_t S>
        friend Array<Type,S> operator*(const Array<Type,S>&, const Array<Type,S>&);

        template<typename Type, size_t S>
        friend Array<Type,S> operator*(const Array<Type,S> , const Type& v);

        template<typename Type, size_t S>
        friend Array<Type,S> operator*(const Type& v, const Array<Type,S>&);
};

//- Template functions definitions must be known before use.
//  Thus included in the header file

template<typename T, size_t N>
Array<T,N>::Array()
:
    std::array<T,N>()
{
};

template<typename T, size_t N>
Array<T,N>::Array(T value)
:
    std::array<T,N>()
{
    this->fill(value);
};

//- operators overloading, declared as friends to Array<T,N> in Array.h

template<typename T, size_t N>
void Array<T,N>::operator+=(const Array<T,N>& p)
{
    for(int i=0; i<N; i++)
    {
        this->operator[](i) += p[i];
    }
};

template<typename T, size_t N>
void Array<T,N>::operator+=(T d)
{
    this->operator+=(Array<T,N>(d));
};

template<typename T, size_t N>
Array<T,N> Array<T,N>::operator+(const T& d)
{
    Array<T,N> tmp = *this;
    tmp+=d;
    return tmp;
}

template<typename T, size_t N>
Array<T,N> Array<T,N>::operator+(const Array<T,N>& p2)
{
    Array<T,N> tmp = *this;
    tmp+=p2;
    return tmp;
}

template<typename T, size_t N>
std::ostream& operator<<(std::ostream& os, const Array<T,N>& p)
{
    os << "(\n";
    for(int i=0; i<N; i++)
    {
        os << '\t' << p[i] << '\n';
    }
    os << ')';

    return os;
}

template<typename Type, size_t S>
Array<Type,S> operator*(const Array<Type,S>& b1, const Array<Type,S>& b2)
{
    Array<Type,S> res;
    for(int i=0; i<b1.size(); i++)
    {
        res[i] = b1[i]*b2[i];
    }
    return res;
}

template<typename Type, size_t S>
Array<Type,S> operator*(const Array<Type,S> b1 , const Type& v)
{
    Array<Type,S> res;
    for(int i=0; i<b1.size(); i++)
    {
        res[i] = b1[i]*v;
    }
    return res;
}

template<typename Type, size_t S>
Array<Type,S> operator*(const Type& v, const Array<Type,S>& b1)
{
    return b1*v;
}
#endif
