import plotly.graph_objects as go
import numpy as np

class SEIRQ:
    def __init__(self, s, e, i, r, q):
        N = s + e + i + r + q
        self.N = N
        self.s = s/N
        self.e = e/N
        self.i = i/N
        self.r = r/N
        self.q = q/N
        
class System:
    def __init__(self, seirq, beta, gamma, delta, theta, eeta, noDays):
        # initial status of the system:
        self.seirq = seirq
        # variables in the system:
        self.beta = beta # PROBABILITY OF INFECTION
        self.gamma = gamma # PROBABILITY OF RECOVERY
        self.delta = delta # PROBABILITY OF USING MASK
        self.theta = theta # PROBABILITY OF SYMPTOMS STARTING
        self.eeta = eeta # PROBABILITY OF QUARANTINE
        # length of the simulation:
        self.noDays = noDays
        
def stepForward(SEIRQ_object, system):
    # past information of the SEIRQ object:
    s = SEIRQ_object.s
    e = SEIRQ_object.e
    i = SEIRQ_object.i
    r = SEIRQ_object.r
    q = SEIRQ_object.q
            
    # create and return new SEIRQ object with the new situation
    
    # Going from S to E:
    infections = system.beta[0]*system.delta*s*i + system.beta[1]*((1-system.delta)*s*i + s*e)
    # Going from E to I or Q:
    symptomatic = system.theta*(1-system.eeta)*e + system.theta*system.eeta*e
    
    s -= infections
    e += infections - symptomatic
    i += system.theta*(1-system.eeta)*e - system.gamma*i
    r += system.gamma*i + system.gamma*q
    q += system.theta*system.eeta*e - system.gamma*q
    
    return SEIRQ(s, e, i, r, q)

def runSimulation(system):
    # four lists: S, E, I, R, and Q, which include all values
    # of the whole simulation day by day
    S = []
    E = []
    I = []
    R = []
    Q = []
    
    # status includes the sir status of the beginning (t0)
    status = system.seirq
    
    # add SIRQ-information of day 0
    t0 = 0
    S.insert(t0, status.s)
    E.insert(t0, status.e)
    I.insert(t0, status.i)
    R.insert(t0, status.r)
    Q.insert(t0, status.q)
    
    for t in range(t0+1, system.noDays):
        status = stepForward(status, system)
        S.insert(t, status.s)
        E.insert(t, status.e)
        I.insert(t, status.i)
        R.insert(t, status.r)
        Q.insert(t, status.q)
    
    # once the loop is ran, return the SEIRQ simulation values
    
    return S, E, I, R, Q

def plotGraphs(S, E, I, R, Q, system):
    # is it interesting to see the graph of E & Q?
    
     # this is used as the x-axis:
    listOfDays = list(range(1, system.noDays+1)) # if noDays=14, range: [1, 2, ..., 13, 14]
    N = system.seirq.N
    
    # Instead of percentages let's take the numbers of individuals:
    S = N*np.asarray(S)
    I = N*np.asarray(I)
    R = N*np.asarray(R)
    
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
    noDays = 60
    # PROBABILITY OF USING MASK
    delta = 0.5 # 50% of the population uses mask
    # PROBABILITY OF INFECTION
    beta = []
    beta1 = 0.3 # 30% if the mask is in use
    beta2 = 0.5 # 50% if there's no mask in use
    beta = [beta1, beta2]
    # PROBABILITY OF SYMPTOMS STARTING
    incubationTime = 5.2
    theta = 1/incubationTime
    # PROBABILITY OF QUARANTINE
    eeta = 0.2 # 40% of the symptomized per day notices infection and self-quarantines    
    # PROBABILITY OF RECOVERY
    recoveryTime = 14
    gamma = 1/recoveryTime
    
    initialSEIRQ = SEIRQ(999, 0, 1, 0, 0)
    system = System(initialSEIRQ, beta, gamma, delta, theta, eeta, noDays)
    
    S, E, I, R, Q = runSimulation(system)
    plotGraphs(S, E, I, R, Q, system)
    print("Simulation finished.")
    
main()