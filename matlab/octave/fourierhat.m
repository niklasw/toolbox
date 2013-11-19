function out=fourierhat(T,x,n)

sum=zeros(1,length(x));
size(sum)
for i=1:n
   if mod(i,2) !=0
      sum += 4/pi*sin(i*x/T)/i;
   end
end

out=sum;
     
