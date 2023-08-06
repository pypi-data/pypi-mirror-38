import scipy
import scipy.special
import random
import math

"""Library to implement hidden Markov Models"""
class Probability(object):
    """Represents a probability as a callable object"""
    
    def __init__(self,n,d):
        """Initialises the probability from a numerator and a denominator"""
        self.Numerator=float(n)
        self.Denominator=float(d)

    def __call__(self):
        """Returns the value of the probability"""
        return self.Numerator/self.Denominator

    def Update(self,deltaN,deltaD):
        """Updates the probability during Bayesian learning"""
        self.Numerator+=deltaN
        self.Denominator+=deltaD

    def __iadd__(self,Prob2):
        """Updates the probability given another Probability object"""
        self.Numerator+=Prob2.Numerator
        self.Denominator+=Prob2.Denominator
        return self

class Distribution(object):
    """ Represents a probability distribution over a set of categories"""
    def __init__(self,categories,k=0):
        """The distribution may be initialised from a list of categories or a
           dictionary of category frequencies. In the latter case, Laplacian
           smoothing may be used"""
        self.Probs={}
        if type(categories).__name__=='dict':
            Denominator=float(len(categories)*k)
            for item in categories:
                Denominator+=float(categories[item])
            self.Probs={item:Probability(categories[item]+k,Denominator) 
                        for item in categories}
        else:
            Denominator=len(categories)
            self.Probs={item:Probability(1,Denominator) 
                        for item in categories}

    def __call__(self,item):
        """Gives the probability of item"""
        return self.Probs[item]()

    def __mul__(self,scalar):
        """Returns the probability of each item, multiplied by a scalar"""
        return Distribution({item:self.Probs[item]()*scalar 
                             for item in self.Probs})

    def __iadd__(self,Dist2):
        """Updates the Distribution given another Distribution with the same states"""
        for state in self.Probs:
            self.Probs[state]+=Dist2.Probs[state]
        return self

    def copy(self):
        """Returns a copy of the Distribution"""
        return Distribution({state:self(state)
                             for state in self.Probs})
    
    def Update(self,categories,weight=None):
        """Updates each category in the probability distiribution, according to
           a dictionary of numerator and denominator values"""
        if weight is None:
            for item in categories:
                self.Probs[item].Update(categories[item])
        else:
            for state in self.Probs:
                self.Probs[state].Update(weight if state==categories else 0.0,weight)

    def Sample(self):
        """Picks a random sample from the distribution"""
        p=random.random()
        Seeking=True
        result=None
        for item in self.Probs:
            x=self(item)
            if Seeking:
                if x>p:
                    Seeking=False
                    result=item
                else:
                    p-=x
        return result

    def States(self):
        """Yields the Distribution's states"""
        for state in self.Probs:
            yield state

    def MaximumLikelihoodState(self):
        """Returns the state with the greatest likelihood"""
        result=None
        Best=0
        for state in self.Probs:
            P=self(state)
            if P>Best:
                result=state
                Best=P
        return result

class PoissonDistribution(Distribution):
    """Represents a Poisson distribution"""
    def __init__(self,mean):
        """Initialises the distribution with a given mean"""
        self.Numerator=float(mean)
        self.Denominator=1.0

    def __call__(self,N):
        """Returns the probability of N"""
        logProb=scipy.log(self.Numerator)-scipy.log(self.Denominator)
        logProb*=N
        logProb-=(self.Numerator/self.Denominator)
        logProb-=scipy.special.gammaln(N+1)
        return scipy.exp(logProb)

    def Update(self,N,p=1.0):
        """Updates the distribution, given a value N that has a probability of P
           of being drawn from this distribution"""
        self.Numerator+=N*p
        self.Denominator+=p

    def Mean(self):
        """Returns the Mean of the PoissonDistribution"""
        return self.Numerator/self.Denominator

    def copy(self):
        """Returns a copy of the PoissonDistribution"""
        return PoissonDistribution(self.Mean)

    def Sample(self):
        """Returns a random sample from the Poisson distribution"""
        p=random.random()
        n=0
        Seeking=True
        while Seeking:
            x=self(n)
            if x>p:
                Seeking=False
            else:
                n+=1
                p-=x
        return n

    def States(self,limit=0.0000001):
        """Yields the PoissonDistribution's states, up to a cumulative
           probability of 1-limit"""
        p=1.0
        n=0
        while p>limit:
            x=self(n)
            yield n
            n+=1
            p-=x

    def MaximumLikelihoodState(self):
        return math.ceil(self.Numerator/self.Denominator)-1
        

class BayesianModel(object):
    """Represents a Bayesian probability model"""
    def __init__(self,Prior,Conditionals):
        """Prior is a Distribution. Conditionals is a dictionary mapping
           each state in Prior to a Distribution"""
        self.Prior=Prior
        self.Conditionals=Conditionals

    def __call__(self,PriorProbs=None):
        """Returns a Distribution representing the probabilities of the outcomes
           given a particular distribution of the priors, which defaults to
           self.Prior"""
        if PriorProbs==None:
            PriorProbs=self.Prior
        Outcomes={}
        for state in PriorProbs.States():
            pH=PriorProbs(state)
            posterior=self.Conditionals[state]
            for outcome in posterior.States():
                Outcomes.setdefault(outcome,0.0)
                Outcomes[outcome]+=posterior(outcome)*pH
        return Distribution(Outcomes)

    def __iadd__(self,Model2):
        """Updates the BayesianModel with the data in another BayesianModel"""
        self.Prior+=Model2.Prior
        for state in self.Conditionals:
            self.Conditionals[state]+=Model2.Conditionals[state]
        return self

    def PriorProbs(self,Observations):
        """Returns a Distribution representing the probabilities of the prior
           states, given a probability Distribution of Observations"""
        return Distribution({state:self.Prior(state)*(sum((self.Conditionals[state](outcome)*Observations(outcome) 
                                                         for outcome in Observations.States())) if isinstance(Observations,Distribution)
                                                                                                 else self.Conditionals[state](Observations))
                             for state in self.Prior.States()})
        
    def MaximumLikelihoodOutcome(self,PriorProbs=None):
        """Returns the maximum likelihood outcome given PriorProbs"""
        return self(PriorProbs).MaximumLikelihoodState()

    def MaximumLikelihoodState(self,Observations=None):
        """Returns the maximum likelihood of the internal state. If Observations
           is None, defaults to the maximum likelihood of the Prior"""
        Probs=self.Prior
        if Observations!=None:
            Probs=self.PriorProbs(Observations)
        return Probs.MaximumLikelihoodState()

    def Outcomes(self):
        """Returns an iterator over the possible outcomes"""
        seen=set()
        for dist in self.Conditionals.values():
            for state in dist.States():
                if state not in seen:
                    seen.add(state)
                    yield state

    def States(self):
        """Returns an iterator over the possible states"""
        return self.Prior.States()


class HMM(BayesianModel):
    """Represents a Hidden Markov Model"""
    def __init__(self,states,outcomes):
        """states is a list or dictionary of states, outcomes is a dictionary
           mapping each state in states to a Distribution of the output states"""
        super(HMM,self).__init__(Distribution(states,1),outcomes)
        self.TransitionProbs=BayesianModel(Distribution(states,1),{state:Distribution(states,1) 
                                                                   for state in states})
        self.Current=None
        self.Previous=None

    def __call__(self,PriorProbs=None):
        """Returns a Distribution of outcomes given PriorProbs, which defaults
           to self.Current if it is set, or self.Prior otherwise"""
        if PriorProbs==None:
            PriorProbs=self.Current
        return super(HMM,self).__call__(PriorProbs)

    def Predict(self):
        """Returns a Distribution representing the probabilities of the next
           state given the current state"""
        if self.Current==None:
            self.Previous=self.Prior.copy()
        else:
            self.Previous=self.Current.copy()
        self.Current=self.TransitionProbs(self.Previous)
        return self.Current

    def PriorProbs(self,Observations):
        """Returns a Distribution the prior probabilities of the HMM's states
           given a Distribution of Observations"""
        if self.Current==None:
            if isinstance(Observations,Distribution):
                self.Current=super(HMM,self).PriorProbs(Observations)
            else:
                self.Current=Distribution({state:self.Prior(state)*self.Conditionals[state](Observations)
                                           for state in self.Prior.States()})
        else:
            if isinstance(Observations,Distribution):
                self.Current=Distribution({state:self.Current(state)*sum((self.Conditionals[state](outcome)*Observations(outcome) 
                                                                          for outcome in Observations.States()))
                                           for state in self.Current.States()})
            else:
                self.Current=Distribution({state:self.Current(state)*self.Conditionals[state](Observations)
                                           for state in self.Current.States()})
        return self.Current

    def Update(self,Observations,use_update=False):
        """Updates the Prior probabilities, TransitionProbs
           and Conditionals given Observations"""
        self.Predict()
        self.PriorProbs(Observations)
        self.Prior+=self.Current
        self.TransitionProbs+=BayesianModel(self.Previous,dict(((state,Distribution(dict(((state2,self.Previous(state)*self.Current(state2)) for state2 in self.Current.States())))) for state in self.Previous.States())))
        for state in self.States():
            if use_update:
                self.Conditionals[state].Update(Observations,self.Current(state))
            else:
                self.Conditionals[state]+=Observations*self.Current(state)

    def Train(self,Sequence,explicit_states=False):
        """Trains the HMM from a sequence of observations"""
        if isinstance(self.Conditionals,dict) and any((isinstance(value,Distribution)
                                                      for value in self.Conditionals.values())):
            ObservableValues=[outcome for outcome in self.Outcomes()]
            if explicit_states:
                for (i,(state,Observation)) in enumerate(Sequence):
                    ObservationProbs=Distribution({Value:1 if Value==Observation else 0 for 
                                                   Value in ObservableValues},0)
                    if i!=0:
                        self.Previous=self.Current
                    self.Current=Distribution({item:1.0 if item==state else 0.0
                                               for item in self.States()})
                    self.Prior+=self.Current
                    self.Conditionals[state]+=ObservationProbs*self.Current(state)
                    if self.Previous is not None:
                        self.TransitionProbs+=BayesianModel(self.Previous,{state:Distribution({state2:self.Previous(state)*self.Current(state2) 
                                                                                               for state2 in self.Current.States()})
                                                                           for state in self.Previous.States()})
            else:
                for (i,Observation) in enumerate(Sequence):
                    ObservationProbs=Distribution(dict(((Value,1 if Value==Observation else 0) for Value in ObservableValues)),0)
                    if i==0:
                        self.PriorProbs(ObservationProbs)
                        self.Prior+=self.Current
                        for state in self.States():
                            self.Conditionals[state]+=ObservationProbs*self.Current(state)
                    else:
                        self.Update(ObservationProbs)
        else:
            if explicit_states:
                for (i,(state,Observation)) in enumerate(Sequence):
                    if i!=0:
                        self.Previous=self.Current
                    self.Current=Distribution({item:1.0 if item==state else 0.0
                                               for item in self.States()})
                    self.Prior+=self.Current
                    self.Conditionals[state].Update(Observation)
                    if self.Previous is not None:
                        self.TransitionProbs+=BayesianModel(self.Previous,{state:Distribution({state2:self.Previous(state)*self.Current(state2) 
                                                                                               for state2 in self.Current.States()})
                                                                           for state in self.Previous.States()})
            else:
                for (i,Observation) in enumerate(Sequence):
                    if i==0:
                        self.PriorProbs(Observation)
                        self.Prior+=self.Current
                        for state in self.States():
                            self.Conditionals[state].Update(Observation,self.Current(state))
                    else:
                        self.Update(Observation,True)
                        
                    

    def Analyse(self,Sequence,MaximumLikelihood=False):
        """Yields the an estimate of the internal states that generated a Sequence
           of observed values, either as the Maximum Likelihood state
           (Maximumlikelihood=True) or as a Distribution (MaximumLikelihood=False)"""
        self.Current=None
        
        for Observation in Sequence:
            
            if MaximumLikelihood:
                yield self.MaximumLikelihoodState(Observation)
            else:
                yield self.PriorProbs(Observation)
            self.Predict()

    def MaximumLikelihoodState(self,Observations=None):
        """Returns the maximum likelihood of the internal state. If Observations
           is None, defaults to the maximum likelihood of the the Current state, or
           the Prior if self.Current is None"""
        Probs=self.Current
        if Probs==None:
            Probs=self.Prior
        if Observations!=None:
            Probs=self.PriorProbs(Observations)
        return Probs.MaximumLikelihoodState()
        
    def P_Observations(self,observation):
        """Returns the probability of an observation given the current
           distribution of hidden states"""
        if self.Current is None:
            self.Current=self.Prior
        return sum((self.Current(state)*self.Conditionals[state](observation)
                    for state in self.Prior.States()))
        

    

    
            

        
           
        
    
            
