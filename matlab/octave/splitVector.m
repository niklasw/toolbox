function out = splitVector(len,n,rank)
%rank from 0 to n-1

if rank >= n
   error='ERR'
   break
end
base = floor(len./n);
rem  = len-base.*n;

starti = 0;
endi   = 0;
if rank < rem
    starti = rank*(base+1);
    mysize = base+1;
    endi   = starti+mysize-1;
else
    starti = rem*(base+1)+(rank-rem)*base;
    mysize = base;
    endi   = starti+mysize-1;
end

limits = [mysize,starti,endi]    


