from pyomo.environ import *

model = ConcreteModel(name="Linear")

A = ["I_C_Scoops", "Peanuts"]
h = {"I_C_Scoops": 1, "Peanuts": 0.1}
d = {"I_C_Scoops": 5, "Peanuts": 27}
c = {"I_C_Scoops": 5, "Peanuts": 27}
u = {"I_C_Scoops": 100, "Peanuts": 40.6}
b = 12

def x_bounds(m, i):
    return (0, u[i])

model.x = Var(A, bounds = x_bounds)

def obj_rule(model):
    return sum(h[i] * (1-u[i]/d[i]**2) * model.x[i] for i in A)

model.z = Objective(rule = obj_rule, sense=maximize)

model.budgetconstr = Constraint(expr = sum(c[i]*model.x[i] for i in A) <= b)

opt = SolverFactory("glpk")
instance = model.create_instance("test.dat")

results = opt.solve(instance)
instance.display()
