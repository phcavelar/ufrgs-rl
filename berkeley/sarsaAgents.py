# sarsaAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# SARSA Agent extension by Anderson Tavares (anderson@dcc.ufmg.br)

# Aluno: 286120

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *
import collections

import random, util, math, itertools

class SarsaAgent(ReinforcementAgent):
    """
      Sarsa Agent
      run with: python gridworld.py -a s -k 100
      (any gridworld run with '-a s' will work, except for the manual agent)
      Useful options:
      --epsilon value
      --edecay value
      --lambda value


      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - computeAction
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    TRACE_MIN_VALUE = 1e-6
    QVALUE_MIN_VALUE = 1e-12
    
    def __init__(self, epsilon_decay=1, lamda=0, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.Qvalues = util.Counter()
        self.lamda = lamda
        
        if self.lamda>0:
            self.traces = util.Counter()
            

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        return self.Qvalues[(state,action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) <= 0:
            return 0.0
        return sorted(
            (self.getQValue(state,a)
                for a in legal_actions),
            reverse=True
        )[0]

    def computeActionFromQValues(self, state):
        """
          Compute the greedy action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) <= 0:
            return None
        actions = sorted(
            ((self.getQValue(state,a), a)
                for a in legal_actions),
            key=lambda x:x[0],
            reverse=True
        )
        best_action = actions[0]
        best_actions = list(itertools.takewhile(
                lambda x: x[0]==best_action[0],
                actions
        ))
        return random.choice(best_actions)[1]

    def computeAction(self, state):
        """
          Compute the action to take in the given state.  With
          probability self.epsilon, take a random action and
          take the greedy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, it
          chooses None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) <= 0:
            return None
        return (
                random.choice(legal_actions)
                if util.flipCoin(self.epsilon)
                else self.computeActionFromQValues(state)
        )

    def getAction(self, state):
        """
          Returns the action computed in computeAction
        """
        return self.computeAction(state)


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        nextAction = self.computeAction(nextState)
        delta = (reward + 
                self.discount * self.getQValue(nextState,nextAction) -
                self.getQValue(state,action)
        )
        if self.lamda==0:
            self.Qvalues[(state,action)] = (
                    self.getQValue(state,action)
                    + self.alpha * delta
            )
        else:
            self.traces[(state,action)] += 1
            vanished = []
            for s,a in self.traces:
                self.Qvalues[(s,a)] = (
                        self.getQValue(s,a)
                        + self.alpha * delta * self.traces[(s,a)]
                )
                
                # Guarding against underflow
                # FIXME Doing this makes the agent not learn anything on pacman
                #if self.getQValue(s,a) < SarsaAgent.QVALUE_MIN_VALUE:
                #    self.Qvalues[(s,a)] = 0.
                
                # Marking small traces for deletion
                self.traces[(s,a)] *= self.lamda * self.discount
                if self.traces[(s,a)] < SarsaAgent.TRACE_MIN_VALUE:
                    vanished.append((s,a))
            # If the action is exit, unmark traces for deletion and clear all traces
            if action == "exit":
                vanished = []
                self.traces.clear()
            for s,a in vanished:
                del self.traces[(s,a)]

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanSarsaAgent(SarsaAgent):
    "Exactly the same as SarsaAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanSarsaAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        SarsaAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of SarsaAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = SarsaAgent.getAction(self, state)
        self.doAction(state,action)
        return action


class ApproximateSarsaAgent(PacmanSarsaAgent):
    """
       ApproximateSarsaAgent

       You should only have to overwrite getQValue
       and update.  All other SarsaAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanSarsaAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        features = self.featExtractor.getFeatures(state,action)
        return sum((features[f]*self.weights[f] for f in features))

    def update(self, state, action, nextState, reward):
        """
                   Should update your weights based on transition
                """
        delta = reward
        features = self.featExtractor.getFeatures(state,action)
        if self.lamda==0:
            for f in features:
                delta += -self.weights[f]
            nextAction = self.computeAction(nextState)
            if nextAction is not None:
                new_features = self.featExtractor.getFeatures(nextState,nextAction)
                for f in new_features:
                    delta += self.discount * self.weights[f]
            for f in features:
                self.weights[f] += self.alpha * delta
        else:
            for f in features:
                delta += -self.weights[f]
                self.traces[f] += features[f]
            nextAction = self.computeAction(nextState)
            if nextAction is not None:
                new_features = self.featExtractor.getFeatures(nextState,nextAction)
                for f in new_features:
                    delta += self.discount * self.weights[f]
            
            vanished = []
            for f in self.traces:
                self.weights[f] += self.alpha * delta * self.traces[f]
                
                # Marking small traces for deletion
                if nextAction is not None:
                    self.traces[f] *= self.lamda * self.discount
                    if self.traces[f] < SarsaAgent.TRACE_MIN_VALUE:
                        vanished.append(f)
            # If the action is exit, unmark traces for deletion and clear all traces
            if action is None or nextAction is None:
                vanished = []
                self.traces.clear()
            for f in vanished:
                del self.traces[f]
                
        

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanSarsaAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
