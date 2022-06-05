import numpy as np
from numpy import asarray
from numpy import exp
from numpy.random import rand
from numpy.random import randint
from numpy.random import seed
from matplotlib import pyplot


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


def neighbor(x, y, z, d, g):
    x_new = x.copy()
    rand_period = randint(1, len(x) + 1)
    print(f'x:{x}')
    print(f'period{rand_period}')
    current_x_t = x[rand_period - 1]
    if current_x_t > 0:
        if rand_period == len(x):
            max_postpone = 0
        else:
            demand_till_period = d[0:rand_period].sum()
            production_till_period = x[0:rand_period].sum()
            max_postpone_prod_demand = production_till_period - demand_till_period
            max_postpone_spare_capacity = (len(x) - rand_period) * g - x[rand_period: len(x)].sum()
            max_postpone = min(max_postpone_prod_demand, max_postpone_spare_capacity)
        print(f'postpone: {max_postpone}')

        if rand_period == 1:
            max_forward = 0
        else:
            max_forward = (rand_period - 1) * g - x[0:rand_period - 1].sum()
        print(f'forward: {max_forward}')
        max_remove = min(current_x_t, max_forward + max_postpone)
        remove_x_t = randint(0, max_remove + 1)
        print(f'remove {remove_x_t}')
        rand_case = rand()
        if rand_case < 0.4:
            # postpone
            print('postpone')
            postpone_x = min(remove_x_t, max_postpone)
            new_x = postpone(x, postpone_x, rand_period, g, True)
            rest = remove_x_t - postpone_x
            if rest > 0:
                new_x = forward(new_x, rest, rand_period, g, True)
        elif rand_case < 0.4:
            # forward
            print('forward')
            forward_x = min(remove_x_t, max_forward)
            new_x = postpone(x, forward_x, rand_period, g, True)
            rest = remove_x_t - forward_x
            if rest > 0:
                new_x = postpone(new_x, rest, rand_period, g, True)
        else:
            print('mix')
            postpone_x = randint(0, min(max_postpone, remove_x_t) + 1)
            print(f'postpone {postpone_x}')
            forward_x = randint(0, min(max_forward, remove_x_t - postpone_x) + 1)
            print(f'forward {forward_x}')
            x_new = postpone(x, postpone_x, rand_period, g, True)
            x_new = forward(x_new, forward_x, rand_period, g, True)
    print(f'd {d}')
    y_new, z_new = feasible_solution(x_new, d)
    return x_new, y_new, z_new


# simulated annealing algorithm
def simulated_annealing(cp, cf, cs, d, g, n_iterations, temp):
    # generate initial point
    x_best = d.copy()
    y_best = np.ones(len(d))
    z_best = np.zeros(len(d))

    # evaluate the initial point
    best_eval = objective(x_best, y_best, z_best, cp, cf, cs)
    # current working solution
    x_curr, y_curr, z_curr, curr_eval = x_best, y_best, z_best, best_eval
    best_scores = list()
    scores = list()
    checked_scores = list()
    # run the algorithm
    for i in range(n_iterations):
        # take a step
        x_cand, y_cand, z_cand = neighbor(x_curr, y_curr, z_curr, d, g)
        # evaluate candidate point
        candidate_eval = objective(x_cand, y_cand, z_cand, cp, cf, cs)
        checked_scores.append(candidate_eval)
        # check for new best solution
        if candidate_eval < best_eval:
            # store new best point
            x_best, y_best, z_best, best_eval = x_cand, y_cand, z_cand, candidate_eval
            # keep track of scores
            best_scores.append(best_eval)
            # report progress
            # print('>%d f(%s) = %.5f' % (i, x_best,y_best,z_best, best_eval))
        # difference between candidate and current point evaluation
        diff = candidate_eval - curr_eval
        # calculate temperature for current epoch
        t = temp / float(i + 1)
        # calculate metropolis acceptance criterion
        metropolis = exp(-diff / t)
        # check if we should keep the new point
        if diff < 0 or rand() < metropolis:
            # store the new current point
            x_curr, y_curr, z_curr, curr_eval = x_cand, y_cand, z_cand, candidate_eval
        scores.append(curr_eval)
    return [x_best, y_best, z_best, best_eval, best_scores, scores, checked_scores]


# seed the pseudorandom number generator
seed(1)

# define the total iterations
n_iterations = 1000

# initial temperature
temp = 10

# cost of production in periods t
cp = asarray([3, 4, 3, 4, 4, 5])
cf = asarray([12, 15, 30, 23, 19, 45])
cs = asarray([1, 1, 1, 1, 1, 1])
# demand per period t
d = asarray([6, 7, 4, 6, 3, 8])
g = 10

# perform the simulated annealing search
best_x, best_y, best_z, score, best_scores, scores, checked_scores = simulated_annealing(cp, cf, cs, d, g, n_iterations, temp)
print('Done!')
print(f'x:{best_x}, y: {best_y}, z:{best_z}')
print(f'score: {score}')
# print('f(%s) = %f' % (best_x, best_y, best_z, score))
# line plot of best scores
pyplot.figure()
pyplot.plot(range(len(best_scores)), best_scores)
pyplot.xlabel('Improvement Number')
pyplot.ylabel('Objective Value')
pyplot.tight_layout()
pyplot.savefig('BestObjValPlot.png')

# line plot of scores
pyplot.figure()
pyplot.plot(range(len(scores)), scores)
pyplot.xlabel('Iteration')
pyplot.ylabel('Objective Value')
pyplot.tight_layout()
pyplot.savefig('ObjValPlot.png')

# line plot of scores
pyplot.figure()
pyplot.plot(range(len(checked_scores)), checked_scores)
pyplot.xlabel('Iteration')
pyplot.ylabel('Evaluated Objective Value')
pyplot.tight_layout()
pyplot.savefig('CheckedObjValPlot.png')

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
