---
title: "Working Note: Construnction speed in popular open-source math modeling tools  "
author: "Shuai Wang"
date: "9/11/2019"
output: html_document
---
In this post, we will compare the popular mathematic programming
language/package: python's pyomo, minizinc, and Juila's JuMP on the context of
model building. Please see the other post for the syntax comparison.

The motivation behind of this is that the model my collegue built using pyomo
costs about 25 minutes just to construct(add variables and constriants). After I read this post


The modeling tools I tested are: python's pyomo, Julia's JuMP, and Minizinc. 
I used CBC as MIP solver.

The problem is from stackoverflow:
[pyomo is slow](https://stackoverflow.com/questions/51269351/pyomo-seems-very-slow-to-write-models),
which states as:

####  set: size = 1..500000
####  variables: x[i], where i in size, float
####   constraints:
$$x[i] >=1,  \forall i \in size$$

####  objective: 
$$Minimize \sum_{i}^{set} x[i]$$


## Here are the scripts:


### Python

```python
  import pyomo.environ as pyo
  import time
  
  size = 500000
  start_time = time.time()
  model = pyo.ConcreteModel()
  model.set = pyo.RangeSet(0, size)
  model.x = pyo.Var(model.set, within=pyo.Reals)
  model.constrList = pyo.ConstraintList()
  
  for i in range(size):
      model.constrList.add(expr = model.x[i] >= 1)
      
  model.obj = pyo.Objective(expr=sum(model.x[i] for i in range(size)), sense=pyo.minimize)
  
  opt = pyo.SolverFactory('cbc', io_format='python')
  
  _time = time.time()
  res = opt.solve(model, report_timing=True)
  print(">>> total time () in {:.2f}s".format(time.time() - start_time))
  print(res)

```

### Julia
```julia
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

```

### Minizinc 
```minizinc 

  int: size = 500000; 
  set of int: N = 1..size;
  
  array[N] of var float: x; 
  constraint forall( n in N)(x[n] >= 1);
  
  var float: objective = sum(n in N)(x[n]);
  solve minimize objective;


```

## Results:

The time consists of constructing and solve time. The actually sovling time are
approximately he same because they all call CBC as solver.

For a simple problem with half million variables and constraints, the resultss
are shown below:

| Tools    | N=500000 | N=1000000 | N=2500000 | N=5000000 |
|----------|----------|-----------|-----------|-----------|
| pyomo    |       28 |        57 |       185 |       377 |
| JuMP     |       36 |        48 |       114 |       450 |
| Minizinc |        9 |        22 |        53 |       109 |


Minizinc is the **fastest**, which also having the best syntax style IMO.


