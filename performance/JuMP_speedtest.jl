import Pkg
using JuMP
using Cbc
using Dates
a = Dates.now()  
N = 500000
m=Model(with_optimizer(Cbc.Optimizer))
@variable(m,x[1:N])
@objective(m, Min, sum(x))
@constraint(m,  x .>= 1)
JuMP.optimize!(m)
b=Dates.now()
print(b-a)
