clear a L l b I
a=input('ange vektornamn (n=udda!!): ');
L=input('ange intervallangd : ');
l=length(a);
h=L/(l-1);
b(1)=1;
for i=2:2:l-1
    b(i)=4;
    b(i+1)=2;
end
b(l)=1;
I=h/3*(dot(a,b))
