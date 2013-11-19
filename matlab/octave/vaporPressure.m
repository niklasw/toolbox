function pout=Pv(t)
% approximating vapour pressure of water
% pv in pascal, t in celsius

pout= 100*6.1121*exp(17.502.*t./(240.97+t));
