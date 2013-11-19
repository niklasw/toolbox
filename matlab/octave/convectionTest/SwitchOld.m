function out=Switch(u,n)
%
%    Jump index n steps forward (1D)
%    Cyclic boundaries
%
     N=length(u);
     tmp = u;
     if n < 0
          n=N+n;
     end

     tmp(n+1:N) = u(1:N-n);
     tmp(1:n) = u(N-n+1:N);

     out = tmp;
