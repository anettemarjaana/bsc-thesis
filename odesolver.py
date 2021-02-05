import numpy as np

class odeSolver:
    def __init__(self, f):
        self.f = f
    
    def step(self):
        # one time step towards the solution
        raise NotImplementedError
        
    def initialize(self, initialValues):
        if isinstance(initialValues, (int, float)):
            # scalar ode
            self.numberOfEqns = 1
            U0 = float(U0)
        else:
            # system of eqns
            initialValues = np.asarray(initialValues)
            self.numberOfEqns = U0.size
        self.U0 = U0
        
    def solve(self, timePoints):
        self.t = np.asarray(timePoints)
        n = self.t.size
        
        self.u = np.zeros((n, self.numberOfEqns))
        
        self.u[0, :] = self.U0
        
        # integrate the derivatives of the model
        for i in range(n - 1):
            self.i = i
            self.u[i + 1] = self.step()
            
        return self.u[:i+2], self.t[i+2]
    
class forwardEuler(odeSolver):
    def step(self):
        u, f, i, t = self.u, self.f, self.i, self.t
        dt = t[i + 1] - t[i]
        
        return u[i, :] + dt * f(u[i, :], t[i])