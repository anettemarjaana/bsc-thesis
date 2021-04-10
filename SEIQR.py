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
        
    def updateValues(self, s, e, i, q, r):
        N = s + e + i + q + r
        self.N = N
        self.s = s/N
        self.e = e/N
        self.i = i/N
        self.q = q/N
        self.r = r/N
 
def stepForward(SEIQR_object, system):
    # past information of the SEIQR object:
    s = SEIQR_object.s
    e = SEIQR_object.e
    i = SEIQR_object.i
    q = SEIQR_object.q
    r = SEIQR_object.r
            
    # create and return new SEIQR object with the new situation
    
    # Going from S to E:
    infections = system.alpha*system.beta[0]*system.delta*(s*e+s*i) + system.beta[1]*(1-system.delta)*(s*e+s*i)
    # Going from E to I or E to Q:
    symptomatic = system.theta*system.eeta*e + system.theta*(1-system.eeta)*e
    
    s -= infections
    e += infections - symptomatic
    i += system.theta*(1-system.eeta)*e - system.gamma*i
    q += system.theta*system.eeta*e - system.gamma*q
    r += system.gamma*i + system.gamma*q
    
    return SEIQR(s, e, i, q, r)
    
class System:
    def __init__(self, seiqr, alpha, delta, eeta, noDays):
        
        # variables in the system:
            
        # PROBABILITY OF INFECTION
        beta = []
        beta1 = 0.6 # 30% if the mask is in use
        beta2 = 1 # 50% if there's no mask in use
        self.beta = [beta1, beta2]
        
        # PROBABILITY OF AN EXPOSED INDIVIDUAL BECOMING SYMPTOMATIC
        incubationTime = 5.2
        self.theta = 1/incubationTime
        
        # PROBABILITY OF RECOVERY AFTER SYMPTOMATIC
        recoveryTime = 10
        self.gamma = 1/recoveryTime
        
        # USER GIVEN VARIABLES:
        self.seiqr = seiqr # initial status of the system
        self.alpha = alpha # MULTIPLIER OF RESTRICTIVE MEASURES
        self.delta = delta # PROBABILITY OF USING MASK
        self.eeta = eeta # PROBABILITY OF QUARANTINE
        self.noDays = noDays # length of the simulation
        
    
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
        
        # add SEIQR-information of day 0
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
        # Instead of percentages let's take the numbers of individuals:
        N = system.seiqr.N
        S = N*np.asarray(S)
        E = N*np.asarray(E)
        I = N*np.asarray(I)
        Q = N*np.asarray(Q)
        R = N*np.asarray(R)
        
        return S, E, I, Q, R
    