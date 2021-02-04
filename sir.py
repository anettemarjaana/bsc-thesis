# SIR disease model

#dS = -beta*S*I
#dI = beta*S*I - gamma*I
#dR = gamma*I

import numpy as np

class SIR:
    def __init__(self, beta, gamma, S0, I0, R0):
        # mu, beta = parameters in the ode system
        # S0, I0, R0 = initial values of the model
        
        # gamma and beta MUST BE FUNCTIONS of t:
            
        if isinstance(beta, (float, int)):
            # if beta is number
            self.beta = lambda t: beta
        elif callable(beta):
            # if beta is function
            self.beta = beta
            
        if isinstance(gamma, (float, int)):
            # if gamma is number
            self.gamma = lambda t: gamma
        elif callable(gamma):
            # if gamma is function
            self.gamma = gamma
            
        
        self.initialValues = [S0, I0, R0]
        
    def __call__(self, u, t):
        
        S, I, R = u
        
        # Return SIR equations    
        return np.asarray([
            -self.beta(t)*S*I,
            self.beta(t)*S*I - self.gamma*I,
            self.gamma*I
            ])