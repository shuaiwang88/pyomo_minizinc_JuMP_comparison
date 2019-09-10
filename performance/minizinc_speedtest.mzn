int: size = 500000; % number of objects
set of int: N = 1..size;

array[N] of var float: x; 
constraint forall( n in N)(x[n] >= 1);

var float: objective = sum(n in N)(x[n]);
solve minimize objective;


