# dynaAgents.py
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

# Dyna Agent support by Anderson Tavares (artavares@inf.ufrgs.br)


from game import *
from learningAgents import ReinforcementAgent

import random,util,math,itertools

class DynaQAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
        - self.plan_steps (number of planning iterations)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, plan_steps=5, kappa=0, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        self.Qvalues = util.Counter()
        
        self.model = dict()
        self.last_visited = dict()
        self.steps_from_beginning = 1
        self.actions_in = dict()
        
        self.plan_steps = plan_steps
        self.kappa = kappa

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
            (self.Qvalues[(state,a)]
                for a in legal_actions),
            reverse=True
        )[0]

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) <= 0:
            return None
        actions = sorted(
            ((self.Qvalues[(state,a)], a)
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

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

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
        
    def _update_q(self, state, action, nextState, reward):
        self.Qvalues[(state,action)] = (
                self.Qvalues[(state,action)]
                + self.alpha * (
                        reward
                        + self.discount * self.computeValueFromQValues(nextState)
                        - self.Qvalues[(state,action)]
                )
        )
        
    def _update_model(self, state, action, nextState, reward):
        self.model[(state,action)] = (nextState,reward)
        if state in self.last_visited:
            self.last_visited[(state,action)] = 0
        else:
            self.last_visited[(state,action)] = 0
            legal_actions = self.getLegalActions(state)
            for untaken_action in [a for a in legal_actions if a!=action]:
                s,a = state,untaken_action
                self.model[(s,a)] = (s,0)
                self.last_visited[(s,a)] = self.steps_from_beginning
            self.actions_in[state] = set(legal_actions)
        if self.kappa>0:
            for s,a in self.model:
                self.last_visited[(s,a)] += 1
            self.steps_from_beginning += 1
            
        
    def _plan(self):
        for i in range(self.plan_steps):
            S,A = random.choice(self.last_visited.keys())
            SS,R = self.model[(S,A)]
            E = self.kappa * self.last_visited[S,A]**0.5
            self._update_q(S,A,SS,R+E)
    

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here.

          NOTE: You should never call this function,
          it will be called on your behalf

          NOTE2: insert your planning code here as well
        """
        self._update_q(state,action,nextState,reward)
        self._update_model(state,action,nextState,reward)
        self._plan()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanDynaQAgent(DynaQAgent):
    "Exactly the same as DynaAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanDynaAgent -a epsilon=0.1

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
        DynaQAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of DynaAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = DynaQAgent.getAction(self, state)
        self.doAction(state,action)
        return action
