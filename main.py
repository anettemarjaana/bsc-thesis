import numpy as np
from odesolver import forwardEuler
from sir import SIR


# This program runs a SIR model based simulation
# of an epidemic. It uses Euler method for approximation
# of the solutions of the differential equations of the model.

def main():
    print("Beginning of simulation")
   #beta changing after a certain number of days:
    #beta = lambda t: 0.0005 if t <= 10 else 0.0001
    
    # Total population, N.
    N = 1000
    # Initial number of infected and recovered individuals, I0 and R0.
    I0, R0 = 1, 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0

    
    # Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
    beta, gamma = 0.2, 1./10 
    # A grid of time points (in days). Here we have 161 days
    # divided into 1000 steps for a more accurate approximation
    timePoints = np.linspace(0, 160, 1000)
    
    # initialize the SIR model with the beginning values:
    sir = SIR(beta, gamma, S0, I0, R0, timePoints)
    
    solver = forwardEuler(sir)
    solver.initialize(sir.initialValues)
        
    u, t = solver.solve(timePoints)
    plotter.plotSIR(u, t)
    print("End of simulation")
    
main()