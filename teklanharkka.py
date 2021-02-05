import matplotlib.pyplot as plt
import numpy as np

class SIR:
    def __init__(self, s, i, r):
        N = s + i + r
        self.s = s/N
        self.i = i/N
        self.r = r/N
        
class System:
    def __init__(self, sir, beta, gamma, t0, tEnd):
        self.sir = sir
        self.beta = beta
        self.gamma = gamma
        self.t0 = t0
        self.tEnd = tEnd
        
def stepForward(SIR_object, system, SIR):
    # past information of the SIR object:
    s = SIR_object.s
    i = SIR_object.i
    r = SIR_object.r
        
    # new infections and recoveries within the past day:
    infections = system.beta*i*s
    recoveries = system.gamma*i
    
    # create and return new SIR object with the new situation
    s -= infections
    i += infections - recoveries
    r += recoveries
    
    return SIR(s, i, r)

def runSimulation(system):
    # three lists: S, I and R, which include all values
    # of the whole simulation
    # status includes the sir status of the beginning (t0)
    status = system.sir
    S = []
    I = []
    R = []
    t0 = system.t0
    S.insert(t0, status.s)
    I.insert(t0, status.i)
    R.insert(t0, status.r)
    
    for t in range(t0, system.tEnd):
        status = stepForward(status, system, SIR)
        S.insert(t+1, status.s)
        I.insert(t+1, status.i)
        R.insert(t+1, status.r)
    
    # once the loop is ran, return the SIR simulation values
    
    return S, I, R

def plotGraphs(S, I, R, system):
    t = np.linspace(system.t0, system.tEnd, len(S))
    fig, ax = plt.subplots()
    lineS = ax.plot(t, S, '--', label="Susceptible")
    lineI = ax.plot(t, I, '--', label="Infectious")
    lineR = ax.plot(t, R, '--', label="Recovered")
    ax.legend(loc = 'upper right')
    plt.xlabel("Time (days)")
    plt.ylabel("Part of the population")
    plt.show()
    
def main():
    t0 = 0
    tEnd = 365
    contacts = 7
    recoveryTime = 14
    beta = 1/contacts
    gamma = 1/recoveryTime
    
    startSIR = SIR(9999, 1, 0)
    system = System(startSIR, beta, gamma, t0, tEnd)
    
    S, I, R = runSimulation(system)
    plotGraphs(S, I, R, system)
    
main()