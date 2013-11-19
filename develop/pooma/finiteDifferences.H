////////////////////////////////////
class myDomain
{
public:
    //constructors
    myDomain
    (
        const Interval<1>& i,
        const Interval<1>& j, 
        const Array<1>& dX,
        const Array<1>& dY
    ){ I=i; J=j; deltaX=dX; deltaY=dY; } 
      
    //Access
    Interval<1> interval(int dir){
        if (!dir){ 
            return I;}
        else{
            return J;}
    }
    Array<1> deltas(int dir){
        if (!dir){ 
            return deltaX;}
        else{
            return deltaY;}
    }

    int size(int dir){
        if (!dir){ 
            return deltaX.length(0);}
        else{
            return deltaY.length(1);}
    }

private:
    Interval<1> I,J;
    Array<1> deltaX,deltaY;        
}

////////////////////////////////////

class fdm
{
public:
    //constructors
    fdm 
    (
        const myDomain & domain
    ){
        deltaX = domain.deltas(0);
        deltaY = domain.deltas(1);
        I = domain.interval(0);
        J = domain.interval(1);
    }

    //members

    Array<2> CD(const Array<2> &a, const int direction){
        int d=direction;
        Array<2> b(a.length(0),a.length(1));
        b = 0;
        if (!d) {
            b(I,J) = (a(I+1,J)-a(I-1,J))/deltaX(I);
        }
        else {
            b(I,J) = a(I,J+1)-a(I,J-1)/deltaY(I);
        }
        return b;
    }

    Array<2> BD(const Array<2> &a, const int direction){
        int d=direction;
        Array<2> b(a.length(0),a.length(1));
        b = 0;
        if (!d) {
            b(I,J) = a(I+1,J)-a(I-1,J);
        }
        else {
            b(I,J) = a(I,J+1)-a(I,J-1);
        }
        return b;
    }


private:
    const Array<1> &deltaX;
    const Array<1> &deltaY;
    const Interval<1> &I;
    const Interval<1> &J;                   
}
