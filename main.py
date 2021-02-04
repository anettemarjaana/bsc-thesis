import numpy as np
from odesolver import forwardEuler
from sir import SIR


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
    
    # initialize the SIR model with the beginning values:
    sir = SIR(beta, gamma, S0, I0, R0)
    
    solver = forwardEuler(sir)
    solver.initialize(sir.initialValues)
        
    # A grid of time points (in days)
    timePoints = np.linspace(0, 160, 160)
    u, t = solver.solve(timePoints)
    plotter.plotSIR(u, t)
    print("End of simulation")
    
main()