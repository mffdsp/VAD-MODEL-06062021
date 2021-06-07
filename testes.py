"""
Minimize the Rosenbrock banana function.

http://en.wikipedia.org/wiki/Rosenbrock_function
"""

import numpy as np
from numpy.random import random
import scipy as scipy
from scipy.optimize import minimize, rosen, rosen_der, root

class Teste:
    def __init__(self):
        self.testinho = 1
    
    def testao(self,x):
        return np.absolute((x[0]-x[1]+x[2])**2)

def funcao2(x):
    return 1/x[0]


def objective(x):
	return np.absolute((x[0] + x[1]**2.0) + 10/x[2])

def func(x): 
   return .5*(1 - x[0])**2 + (x[1] - x[0]**2)**2 

def func2(x):   # The rosenbrock function
    j = func(x)
    return j
    # return .5*(1 - x[0])**2 + (x[1] - x[0]**2)**2


teste = Teste()
result = minimize(funcao2, [10], method='SLSQP')
A = [1,2,3,4]
B = [5,3,5,5]
print(np.dot(A,B))
# solution =  list(map(lambda x: round(x,2), result['x']))
# evaluation = funcao2(solution) 

# # COS
# intervalo = ((0, 10) , (0,10))
# result = minimize(func2, [1,1], method="trust-constr", bounds=intervalo)

# solution = list(map(lambda x: round(x,2), result['x']))

# evaluation = round(func2(solution),2)

# print(result) 
# print('\n'*2)
# print('Success: %s' % result['success'])
# print('f[{parametros}] = {resultados}' .format(parametros=solution, resultados=evaluation))
# print('\n'*2)


