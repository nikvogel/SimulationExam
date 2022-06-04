import numpy as np
from numpy import asarray
from numpy import exp
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed
from matplotlib import pyplot


# objective function
def objective(x,y,z,cp,cf,cs):
    return np.sum(cp*x)+np.sum(cf*y)+np.sum(cs*z)

def neighbor(x,y,z):
    #TODO
    return x,y,z

# simulated annealing algorithm
def simulated_annealing(objective, cp, cf, cs, d, n_iterations, step_size, temp):
    # generate initial point
    x_best = d
    y_best = np.ones(len(d))
    z_best = np.zeros(len(d))

    # evaluate the initial point
    best_eval = objective(x_best, y_best, z_best, cp, cf, cs)
    # current working solution
    x_curr, y_curr, z_curr, curr_eval = x_best, y_best, z_best, best_eval
    scores = list()
    # run the algorithm
    for i in range(n_iterations):
        # take a step
        x_cand, y_cand, z_cand = neighbor( x_curr, y_curr, z_curr)
        # evaluate candidate point
        candidate_eval = objective(x_cand, y_cand, z_cand, cp, cf, cs)
        # check for new best solution
        if candidate_eval < best_eval:
            # store new best point
            best_x, best_y, best_z, best_eval = x_cand, y_cand, z_cand, candidate_eval
            # keep track of scores
            scores.append(best_eval)
            # report progress
            print('>%d f(%s) = %.5f' % (i, x_best,y_best,z_best, best_eval))
        # difference between candidate and current point evaluation
        diff = candidate_eval - curr_eval
        # calculate temperature for current epoch
        t = temp / float(i + 1)
        # calculate metropolis acceptance criterion
        metropolis = exp(-diff / t)
        # check if we should keep the new point
        if diff < 0 or rand() < metropolis:
            # store the new current point
            x_curr, y_curr, z_curr, curr_eval = x_cand, y_cand, z_cand,candidate_eval
    return [x_best, y_best, z_best, best_eval, scores]


# seed the pseudorandom number generator
seed(1)

# define the total iterations
n_iterations = 1000

# define the maximum step size
step_size = 0.1

# initial temperature
temp = 10

#cost of production in periods t
cp = asarray([3,4,3,4,4,5])
cf = asarray([12,15,30,23,19,45])
cs = asarray([1,1,1,1,1,1])
#demand per period t
d = asarray([6,7,4,6,3,8])


# perform the simulated annealing search
best_x, best_y, best_z, score, scores = simulated_annealing(objective, cp, cf, cs, d, n_iterations, step_size, temp)
print('Done!')
print(f'x:{best_x}, y: {best_y}, z:{best_z}')
#print('f(%s) = %f' % (best_x, best_y, best_z, score))
# line plot of best scores
pyplot.plot(scores, '.-')
pyplot.xlabel('Improvement Number')
pyplot.ylabel('Evaluation f(x)')
pyplot.show()