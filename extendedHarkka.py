import plotly.graph_objects as go
import numpy as np

class SIRQ:
    def __init__(self, s, i, r, q):
        N = s + i + r + q
        self.s = s/N
        self.i = i/N
        self.r = r/N
        self.q = q/N
        
class System:
    def __init__(self, sirq, beta, gamma, delta, eeta, noDays):
        self.sirq = sirq
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.eeta = eeta
        self.noDays = noDays
        
def stepForward(SIRQ_object, system):
    # past information of the SIRQ object:
    s = SIRQ_object.s
    i = SIRQ_object.i
    r = SIRQ_object.r
    q = SIRQ_object.q
        
    # new infections and recoveries within the past day:
    infections = system.beta[0]*system.delta*s*i + system.beta[1]*(1-system.delta)*s*i
    recoveries = system.gamma*i + system.gamma*q
    quarantines = system.eeta*i - system.gamma*q
    
    # create and return new SIR object with the new situation
    s -= infections
    i += infections - recoveries - quarantines
    r += recoveries
    q += quarantines
    
    return SIRQ(s, i, r, q)

def runSimulation(system):
    # four lists: S, I, R, and Q, which include all values
    # of the whole simulation day by day
    S = []
    I = []
    R = []
    Q = []
    
    # status includes the sir status of the beginning (t0)
    status = system.sirq
    
    # add SIRQ-information of day 0
    t0 = 0
    S.insert(t0, status.s)
    I.insert(t0, status.i)
    R.insert(t0, status.r)
    Q.insert(t0, status.q)
    
    for t in range(t0+1, system.noDays):
        status = stepForward(status, system)
        S.insert(t, status.s)
        I.insert(t, status.i)
        R.insert(t, status.r)
        Q.insert(t, status.q)
    
    # once the loop is ran, return the SIRQ simulation values
    
    return S, I, R, Q

def plotGraphs(S, I, R, system):
    # is it interesting to see the graph of Q?
    
    #print("\n\nNumbers of susceptible: ", S, "length: ", len(S))
    #print("Numbers of infected: ", I, "length: ", len(I))
    #print("Numbers of resistant: ", R, "length: ", len(R))
    
     # this is used as the x-axis:
    listOfDays = list(range(1, system.noDays+1)) # if noDays=14, range: [1, 2, ..., 13, 14]
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x = listOfDays,
            y = S,
            name = "S",
            mode = 'lines',
            marker = dict(
                color = "#009E73"
            )
        ))

    fig.add_trace(
        go.Scatter(
            x = listOfDays,
            y = I,
            name = "I",
            mode = 'lines',
            marker = dict(
                color = "#D55E0D"
            )
        ))
    
    fig.add_trace(
        go.Scatter(
            x = listOfDays,
            y = R,
            name = "R",
            mode = 'lines',
            marker = dict(
                color = "#0072B2"
            )
        ))
    
    fig.update_layout(
        title="Tartunnan leviäminen populaatiossa",
        xaxis=dict(
            title='Päivä',
            tickmode='linear'),
        yaxis_title="Tapausten lukumäärä",
        legend_title="Kuvaajat",
        font=dict(
            size=12
        )
    )
    
    fig.show()
    
def main():
    # SIMULATION LENGTH
    noDays = 90
    # PROBABILITY OF USING MASK
    delta = 0.5 # 50% of the population uses mask
    # PROBABILITY OF INFECTION
    beta = []
    beta1 = 0.3 # 30% if the mask is in use
    beta2 = 0.5 # 50% if there's no mask in use
    beta = [beta1, beta2]
    # PROBABILITY OF QUARANTINE
    eeta = 0.1 # 10% of the infected per day notices infection and self-quarantines    
    # PROBABILITY OF RECOVERY
    recoveryTime = 14
    gamma = 1/recoveryTime
    
    startSIRQ = SIRQ(9999, 1, 0, 0)
    system = System(startSIRQ, beta, gamma, delta, eeta, noDays)
    
    S, I, R, Q = runSimulation(system)
    plotGraphs(S, I, R, system)
    print("Simulation finished.")
    
main()