import numpy as np
from numpy import asarray
from numpy import exp
from numpy.random import rand
from numpy.random import randint
from numpy.random import seed
from matplotlib import pyplot
import pandas as pd
from exact_solution import get_exact_solution


# objective function
def objective(x, y, z, cp, cf, cs):
    return np.sum(cp * x) + np.sum(cf * y) + np.sum(cs * z)


def postpone(x, amount, time_period, g, less):
    x_new = x.copy()
    if amount > 0:
        x_new[time_period - 1] = x[time_period - 1] - amount
        while amount > 0:
            next_period = min(amount, g - x[time_period])
            x_new[time_period] = x[time_period] + next_period
            amount = amount - next_period
            time_period -= 1
    return x_new


def forward(x, amount, time_period, g,less):
    x_new = x.copy()
    if amount > 0:
        x_new[time_period - 1] = x[time_period - 1] - amount
        while amount > 0:
            next_period = min(amount, g - x[time_period - 2])
            x_new[time_period - 2] = x[time_period - 2] + next_period
            amount = amount - next_period
            time_period -=1
    return x_new


def feasible_solution(x, demand):
    y = np.zeros(len(x))
    z = np.zeros(len(x))
    for i in range(0, len(x)):
        if x[i] > 0:
            y[i] = 1
        else:
            pass
        if i == 0:
            z[i] = x[i] - demand[i]
        else:
            z[i] = z[i - 1] + x[i] - demand[i]
    return y, z


def neighbor(x, y, z, d, g, temp, t):
    x_new = x.copy()
    current_x_t = 0
    while current_x_t < 1:
        rand_period = randint(1, len(x) + 1)
        current_x_t = x[rand_period - 1]
    random_case = rand()
    if random_case < 0.3 and t < 0.3* temp:
        current_x_t2 = 0
        second_period = 0
        while current_x_t2 < 1 and rand_period != second_period:
            second_period = randint(1, len(x) + 1)
            current_x_t2 = x[second_period - 1]
        if rand_period > second_period: # forward production
            max_forward = min(g-x[second_period-1], current_x_t2)
            if max_forward > 0:
                x_forward = randint(1, max_forward+1)
                x_new[rand_period-1] = x[rand_period-1] - x_forward
                x_new[second_period-1] = x[second_period-1] + x_forward
        else: # postpone production
            max_postpone_production = min(g-x[second_period-1], x[rand_period-1])
            max_postpone_demand = x[rand_period-1]
            for t in range(rand_period-1, second_period):
                demand_till_period = d[0:t].sum()
                production_till_period = x[0:t].sum()
                max_postpone_demand = min(production_till_period - demand_till_period, max_postpone_demand)
            max_postpone = min(max_postpone_demand, max_postpone_production)
            if max_postpone > 0:
                x_postpone = randint(1, max_postpone + 1)
                x_new[rand_period-1] = x[rand_period-1] - x_postpone
                x_new[second_period-1] = x[second_period-1] + x_postpone
    if rand_period == len(x):
        max_postpone = 0
    else:
        demand_till_period = d[0:rand_period].sum()
        production_till_period = x[0:rand_period].sum()
        max_postpone_prod_demand = production_till_period - demand_till_period
        max_postpone_spare_capacity = (len(x) - rand_period) * g - x[rand_period: len(x)].sum()
        max_postpone = min(max_postpone_prod_demand, max_postpone_spare_capacity)
    if rand_period == 1:
        max_forward = 0
    else:
        max_forward = (rand_period - 1) * g - x[0:rand_period - 1].sum()
    max_remove = min(current_x_t, max_forward + max_postpone)
    if max_remove > 0:
        remove_x_t = randint(1, max_remove + 1)
        if t > 0.5*temp:
            case = rand()
            if case < 0.3:
                remove_x_t = max_remove
    else:
        remove_x_t = 0
    rand_case = rand()
    if rand_case < 0.5:
        # postpone
        postpone_x = min(remove_x_t, max_postpone)
        x_new = postpone(x, postpone_x, rand_period, g, True)
        rest = remove_x_t - postpone_x
        if rest > 0:
            x_new = forward(x_new, rest, rand_period, g, True)
    elif rand_case < 1:
        # forward
        forward_x = min(remove_x_t, max_forward)
        x_new = forward(x, forward_x, rand_period, g, True)
        rest = remove_x_t - forward_x
        if rest > 0:
            x_new = postpone(x_new, rest, rand_period, g, True)
    else:
        postpone_x = randint(0, min(max_postpone, remove_x_t) + 1)
        forward_x = randint(0, min(max_forward, remove_x_t - postpone_x) + 1)
        x_new = postpone(x, postpone_x, rand_period, g, True)
        x_new = forward(x_new, forward_x, rand_period, g, True)
    y_new, z_new = feasible_solution(x_new, d)
    return x_new, y_new, z_new



# simulated annealing algorithm
def simulated_annealing(cp, cf, cs, d, g, n_iterations, temp):
    # generate initial point
    x_best = d.copy()
    y_best = np.ones(len(d))
    z_best = np.zeros(len(d))

    best_scores = list()
    scores = list()
    checked_scores = list()
    checked_x = list()
    improvement_iterations = list()

    # evaluate the initial point
    best_eval = objective(x_best, y_best, z_best, cp, cf, cs)
    best_scores.append(best_eval)
    scores.append(best_eval)
    checked_scores.append(best_eval)
    # current working solution
    x_curr, y_curr, z_curr, curr_eval = x_best, y_best, z_best, best_eval
    checked_x.append(x_curr)
    # run the algorithm
    for i in range(n_iterations):
        # calculate temperature for current epoch
        t = temp * (0.8**i)
        # take a step
        x_cand, y_cand, z_cand = neighbor(x_curr, y_curr, z_curr, d, g, temp, t)
        checked_x.append(x_cand)
        # evaluate candidate point
        candidate_eval = objective(x_cand, y_cand, z_cand, cp, cf, cs)
        checked_scores.append(candidate_eval)
        # check for new best solution
        if candidate_eval < best_eval:
            # store new best point
            x_best, y_best, z_best, best_eval = x_cand, y_cand, z_cand, candidate_eval
            # keep track of scores
            best_scores.append(best_eval)
            improvement_iterations.append(i)
        # difference between candidate and current point evaluation
        diff = candidate_eval - curr_eval
        
        # calculate metropolis acceptance criterion
        metropolis = exp(-diff / t)
        # check if we should keep the new point
        if diff < 0 or rand() < metropolis:
            # store the new current point
            x_curr, y_curr, z_curr, curr_eval = x_cand, y_cand, z_cand, candidate_eval
        scores.append(curr_eval)
    return [x_best, y_best, z_best, best_eval, best_scores, scores, checked_scores, checked_x, improvement_iterations]


# seed the pseudorandom number generator
seed(0)

# define the total iterations
n_iterations = 1000

# initial temperature
t = 1
temp = 1

# cost of production in periods t
cp = asarray([3, 4, 3, 4, 4, 5])
cf = asarray([12, 15, 30, 23, 19, 45])
cs = asarray([1, 1, 1, 1, 1, 1])
# demand per period t
d = asarray([6, 7, 4, 6, 3, 8])
g = 10

# exact solution
x_opt, obj_opt = get_exact_solution(cp, cf, cs, d, g)
print(f'x opt: {np.round(x_opt,1)}')
print(f'obj val: {obj_opt}')

# perform the simulated annealing search
best_score_per_seed = list()
iterrations_for_best_per_seed = list()

for i in range(100):
    seed(i)
    best_x, best_y, best_z, score, best_scores, scores, checked_scores, checked_x, improvement_iterations = simulated_annealing(cp, cf, cs, d, g, n_iterations, temp)
    best_score_per_seed.append(score)
    iterrations_for_best_per_seed.append(improvement_iterations[-1])
    print('Done!')
    print(f'x:{best_x}, y: {best_y}, z:{best_z}')
    print(f'score: {score}')

print(f'Best average: {np.mean(best_score_per_seed)}')
print(f'Max score: {max(best_score_per_seed)}')
print(f'Iterations average: {np.mean(iterrations_for_best_per_seed)}')


# print('f(%s) = %f' % (best_x, best_y, best_z, score))

# line plot of best scores
pyplot.figure()
pyplot.plot(range(len(best_scores)), best_scores)
pyplot.xlabel('Improvement Number')
pyplot.ylabel('Objective Value')
pyplot.tight_layout()
pyplot.savefig('BestObjValPlot.png')

# line plot of current scores
pyplot.figure()
pyplot.plot(range(len(scores)), scores)
pyplot.xlabel('Iteration')
pyplot.ylabel('Objective Value')
pyplot.tight_layout()
pyplot.savefig('ObjValPlot.png')

# line plot of checked scores
pyplot.figure()
pyplot.plot(range(len(checked_scores)), checked_scores)
pyplot.xlabel('Iteration')
pyplot.ylabel('Evaluated Objective Value')
pyplot.tight_layout()
pyplot.savefig('CheckedObjValPlot.png')

# line plot of checked x
pyplot.figure()
pyplot.plot(range(30), checked_x[:30], label = ['x1','x2','x3','x4','x5','x6'])
pyplot.xlabel('Iteration')
pyplot.ylabel('X Values')
pyplot.legend()
pyplot.tight_layout()
pyplot.savefig('CheckedXPlot.png')

# plot of solution
pyplot.figure()
pyplot.plot(range(1,7), best_x, label='Production')
pyplot.plot(range(1,7), best_z, label= 'Storage')
pyplot.plot(range(1,7), d, label = 'Demand')
pyplot.ylabel('Amount')
pyplot.xlabel('Period')
pyplot.legend()
pyplot.tight_layout()
pyplot.savefig('PlotSolutionSA.png')
