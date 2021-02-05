# SIR disease model

#dS = -beta*S*I
#dI = beta*S*I - gamma*I
#dR = gamma*I

import numpy as np

class SIR:
    def __init__(self, beta, gamma, S0, I0, R0, timePoints):
        # mu, beta = parameters in the ode system
        # S0, I0, R0 = initial values of the model
        
        self.beta = beta
        self.gamma = gamma
        self.initialValues = [S0, I0, R0]
        self.t = np.asarray(timePoints)
        
    def getEquations(self, sirValues):
        S, I, R = sirValues
        # Return SIR equations  
        return np.asarray([
            -self.beta*S*I,
            self.beta*S*I - self.gamma*I,
            self.gamma*I
            ]) 
                   
    def solve(self):
        # number of time steps in the simulation:
        noTimeSteps = self.t.size
        
        self.u = np.zeros((noTimeSteps, self.numberOfEqns))
        
        self.u[0, :] = self.U0
        
        # integrate the derivatives of the model
        for i in range(n - 1):
            self.i = i
            self.u[i + 1] = self.step()
            
        return self.u[:i+2], self.t[i+2]
    
    def forwardEuler(odeSolver):
        u, f, i, t = self.u, self.f, self.i, self.t
        dt = t[i + 1] - t[i]
        
        return u[i, :] + dt * f(u[i, :], t[i])