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
print("the model buid" time.time() -a)
print(">>> total time () in {:.2f}s".format(time.time() - _time))
print(time.time() -a)
print(res)
