function out=heaviside(x,p)

N=length(x);
for i = 1:N
     if x(i) < p
          out(i)=0;
     else
          out(i)=1;
     end
end
out = out';
