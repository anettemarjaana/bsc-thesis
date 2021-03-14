import plotly.graph_objects as go
import numpy as np

class SEIQR:
    def __init__(self, s, e, i, q, r):
        N = s + e + i + q + r
        self.N = N
        self.s = s/N
        self.e = e/N
        self.i = i/N
        self.q = q/N
        self.r = r/N
        
class System:
    def __init__(self, seiqr, alpha, beta, gamma, delta, theta, eeta, noDays):
        # initial status of the system:
        self.seiqr = seiqr
        # variables in the system:
        self.alpha = alpha # MULTIPLIER OF RESTRICTIVE MEASURES
        self.beta = beta # PROBABILITY OF INFECTION
        self.gamma = gamma # PROBABILITY OF RECOVERY
        self.delta = delta # PROBABILITY OF USING MASK
        self.theta = theta # PROBABILITY OF SYMPTOMS STARTING
        self.eeta = eeta # PROBABILITY OF QUARANTINE
        # length of the simulation:
        self.noDays = noDays
        
def stepForward(SEIQR_object, system):
    # past information of the SEIQR object:
    s = SEIQR_object.s
    e = SEIQR_object.e
    i = SEIQR_object.i
    q = SEIQR_object.q
    r = SEIQR_object.r
            
    # create and return new SEIQR object with the new situation
    
    # Going from S to E:
    infections = system.beta[0]*system.delta*s*i + system.beta[1]*((1-system.delta)*s*i)
    # Going from E to I or Q:
    symptomatic = system.theta*system.eeta*e + system.theta*(1-system.eeta)*e
    
    s -= infections
    e += infections - symptomatic
    i += system.theta*(1-system.eeta)*e - system.gamma*i
    q += system.theta*system.eeta*e - system.gamma*q
    r += system.gamma*i + system.gamma*q
    
    return SEIQR(s, e, i, q, r)

def runSimulation(system):
    # four lists: S, E, I, Q, and R, which include all values
    # of the whole simulation day by day
    S = []
    E = []
    I = []
    Q = []
    R = []
    
    # status includes the sir status of the beginning (t0)
    status = system.seiqr
    
    # add SIRQ-information of day 0
    t0 = 0
    S.insert(t0, status.s)
    E.insert(t0, status.e)
    I.insert(t0, status.i)
    Q.insert(t0, status.q)
    R.insert(t0, status.r)
    
    for t in range(t0+1, system.noDays):
        status = stepForward(status, system)
        S.insert(t, status.s)
        E.insert(t, status.e)
        I.insert(t, status.i)
        Q.insert(t, status.q)
        R.insert(t, status.r)
    
    # once the loop is ran, return the SEIQR simulation values
    
    return S, E, I, Q, R

def plotGraphs(S, E, I, Q, R, system):
    # is it interesting to see the graph of E & Q?
    
     # this is used as the x-axis:
    listOfDays = list(range(1, system.noDays+1)) # if noDays=14, range: [1, 2, ..., 13, 14]
    N = system.seiqr.N
    
    # Instead of percentages let's take the numbers of individuals:
    S = N*np.asarray(S)
    E = N*np.asarray(E)
    I = N*np.asarray(I)
    Q = N*np.asarray(Q)
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
            y = E,
            name = "E",
            mode = 'lines',
            marker = dict(
                color = "#FFC107"
            ),
            line={"width": 0.5},
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
            y = Q,
            name = "Q",
            mode = 'lines',
            marker = dict(
                color = "#082F29"
            ),
            line={"width": 0.5},
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
        title="The spread of COVID-19 (SEIQR-model)",
        xaxis=dict(
            title='Day'),
        yaxis_title="Number of cases",
        legend_title="Graphs",
        font=dict(
            size=12
        )
    )
    
    fig.show()
    
def main():
    # INPUTS OF THE SEIQR MODEL entered by user with the sliders:
    
    # SIMULATION LENGTH
    noDays = 60
    # POLITICAL RESTRICTIONS
    alpha = 1 # the smaller value, the more strict the restrictions are
    # PROBABILITY OF USING MASK
    delta = 0.4 # 50% of the population uses mask
    # PROBABILITY OF INFECTION
    beta = []
    beta1 = 0.3 # 30% if the mask is in use
    beta2 = 0.7 # 50% if there's no mask in use
    beta = [beta1, beta2]
    # PROBABILITY OF AN INFECTED INDIVIDUAL BECOMING INFECTIOUS
    incubationTime = 1.3
    theta = 1/incubationTime
    # PROBABILITY OF QUARANTINE
    eeta = 0.2 # 20% of the infectious per day notices infection and self-quarantines    
    # PROBABILITY OF RECOVERY
    recoveryTime = 14
    gamma = 1/recoveryTime
    
    initialSEIQR = SEIQR(999, 0, 1, 0, 0)
    system = System(initialSEIQR, alpha, beta, gamma, delta, theta, eeta, noDays)
    
    S, E, I, Q, R = runSimulation(system)
    plotGraphs(S, E, I, Q, R, system)
    print("Simulation finished.")
    
main()