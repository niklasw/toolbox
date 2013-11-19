close all
clear all

size=100;

dt=.005;
tol=1e-5
nReinit=50;
nReinit2=5;
epsilon=.01;

O2terms=1

x=linspace(0,1,size);
dx=x(2:size)-x(1:size-1);
dx(size)=dx(size-1);
d=sin(6*pi*x.^2).*sqrt(x);
%d=d+d*.1.*sin(30*pi*x);
d0=d;
%%%%%% FIND INTERFACES BEFORE REINIT
n=0;
for i=2:size-1
	dp=d(i);db=d(i-1);rdx=1/dx(i);
	Db(i)=rdx*(dp-db);
	if not(sign(d(i)) == sign(d(i-1)))
		n=n+1;
		roots0(n)=x(i)-d(i)/Db(i);
	end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%

subplot(211)
plot(x,d);
grid

stepper=0;errSum=10;

%%%%%%% THE TIME LOOP STARTS HERE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%while and(errSum > tol,stepper<100)
while stepper < nReinit

dOld=d;

%%%%%% FIRST DERIVATIVES
for i=2:size-1
	dp=d(i);db=d(i-1);df=d(i+1);
	rdx=1/dx(i);
	Db(i)=rdx*(dp-db);
	Df(i)=rdx*(df-dp);
	Dc(i)=.5*rdx*(df-db);
end
Db(1)=Db(2);Db(size)=Db(size-1);
Df(1)=Df(2);Df(size)=Df(size-1);
Dc(1)=Dc(2);Dc(size)=Dc(size-1);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%% SECOND DERIVATIVES
for i=2:size-1
	DD(i)=rdx*(Df(i)-Df(i-1));	
end
DD(1)=DD(2);DD(size)=DD(size-1);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%% MINMOD
for i=2:size-1
	if DD(i)*DD(i-1) > 0
		O2term1(i)=sign(DD(i))*min(abs(DD(i)),abs(DD(i-1)));
	else
		O2term1(i)=0;
	end
	
	if DD(i+1)*DD(i) > 0
		O2term2(i)=sign(DD(i+1))*min(abs(DD(i+1)),abs(DD(i)));
	else
		O2term2(i)=0;
	end
end
O2term1(1)=O2term1(2);O2term1(size)=O2term1(size-1);
O2term2(1)=O2term2(2);O2term2(size)=O2term2(size-1);

if not(O2terms)
	O2term1=zeros(1,size);
	O2term2=zeros(1,size);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:size-1
	p_(i)=Db(i)+.5*dx(i)*O2term1(i);
	pp(i)=Db(i+1)+.5*dx(i)*O2term2(i);
end
pp(size)=pp(size-1);
p_(size)=p_(size-1);

for i=1:size
	PP(i)=sqrt(max(p_(i),0)^2+min(pp(i),0)^2);
	P_(i)=sqrt(min(p_(i),0)^2+max(pp(i),0)^2);
end

for i=1:size	
	if d(i)<=0
		absD(i)=P_(i);
	else
		absD(i)=PP(i);
	end
end
epsilon=abs(Dc).^2.*dx.^2;
Sign=dOld./sqrt(dOld.^2+epsilon.^2); 

d=d+dt*Sign.*(1-absD);

errSum=sum(abs(dOld-d))/size;
errMax=max(abs(dOld-d));
stepper = stepper+1;

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


subplot(212)
plot(x,d,'r',x,0,'+');
grid
zoom

%%figure
%%plot(x,Db,'r',x,Df,'b',x,Dc,'g')
%%plot(x,PP,'r',x,P_,'g')

%%%%%% FIND INTERFACES
n=0;
for i=2:size-1
	if not(sign(d(i)) == sign(d(i-1)))
		n=n+1;
		roots(n)=x(i)-d(i)/Db(i);
	end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%

stepper
errMax

format long
[roots0',roots',(roots0-roots)']

format short