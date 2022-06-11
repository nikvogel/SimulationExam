import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import scipy.sparse as sp
import matplotlib.pyplot as plt


def get_exact_solution(cp, cf, cs, d, g):
    time_periods = np.arange(1, len(d) + 1)
    model = gp.Model('ProductionMgmtProblem')

    x = model.addVars(time_periods, vtype=GRB.CONTINUOUS, name='x_')
    y = model.addVars(time_periods, vtype=GRB.BINARY, name='y_')
    z = model.addVars(np.arange(0, len(d) + 1), vtype=GRB.CONTINUOUS, name='z_')

    model.setObjective(gp.quicksum(x[t] * cp[t - 1] for t in time_periods)
                       + gp.quicksum(y[t] * cf[t - 1] for t in time_periods)
                       + gp.quicksum(z[t] * cs[t - 1] for t in time_periods), GRB.MINIMIZE)

    model.addConstrs(z[t - 1] + x[t] == d[t - 1] + z[t] for t in time_periods)

    model.addConstrs(x[t] <= g * y[t] for t in time_periods)

    model.addConstr(z[0] == 0)

    model.optimize()

    obj_value = model.objVal

    x_star = []
    y_star = []
    z_star = []
    for t in time_periods:
        x_star.append(x[t].x)
        y_star.append(y[t].x)
        z_star.append(z[t].x)

    return x_star, obj_value