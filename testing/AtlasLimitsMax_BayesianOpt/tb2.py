import numpy as np
from bayes_opt import BayesianOptimization
import matplotlib.pyplot as plt
from scipy.optimize import NonlinearConstraint

if __name__ == '__main__':
    def target_function(x, y, z, w, u):
        # Gardner is looking for the minimum, but this packages looks for maxima, thus the sign switch
        returnVal = np.cos(2*x)*np.cos(y) + np.sin(x) + np.tan(z) - np.cos(w) + np.tan(u)**2
        print(f'allowed: {returnVal}\n \
x: {(x)}, y: {(y)}, z: {(z)}, w: {(w)}, u: {(u)}\n')

        return np.cos(2*x)*np.cos(y) + np.sin(x)

    def constraint_function(x, y, z, w, u):
        constrVal = np.cos(x) * np.cos(y) - np.sin(x) * np.sin(y) + np.cos(z)**2 + np.tan(w*u)
        
        if constrVal > 0:
            returnVal = 1

        elif constrVal <= 0:
            returnVal = -1
        
        else: raise Exception('something went wrong...')
        
        print(f'constraint: {constrVal}, constraint return: {returnVal}\n \
x: {(x)}, y: {(y)}, z: {(z)}, w: {(w)}, u: {(u)}\n')

        return returnVal


    constraint = NonlinearConstraint(constraint_function, 0, np.inf)

    # Bounded region of parameter space
    pbounds = {'x': (-np.pi/2, np.pi/2), 'y': (-np.pi/2, np.pi/2), 
               'z': (-np.pi/2, np.pi/2), 'w': (-np.pi/2, np.pi/2),
               'u': (-np.pi/2, np.pi/2)}

    optimizer = BayesianOptimization(
        f=target_function,
        constraint=constraint,
        pbounds=pbounds,
        verbose=0, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
        random_state=1,
    )

    optimizer.maximize(
        init_points=5,
        n_iter=10,
    )
    #maxs_.append(optimizer.max['target'])
#print(maxs_) 
    print(optimizer.max)

# Out: [1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493, 1.7926580410885493



























































