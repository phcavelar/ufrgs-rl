# valueIterationAgents.py
# -----------------------
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

# Aluno: 286120

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    * Please read learningAgents.py before reading this.*

    A ValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs value iteration
    for a given number of iterations using the supplied
    discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, inplace=False):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        self.error = 0
        for i in range(self.iterations):
            self.error = 0
            if not inplace:
                old_values = self.values.copy()
            for s in self.mdp.getStates():
                v = self.values[s] if inplace else old_values[s]
                possible_actions = self.mdp.getPossibleActions(s)
                if len(possible_actions)<=0:
                    continue
                self.values[s] = max(
                    (sum(
                        p * (self.mdp.getReward(s,a,ss) +
                            self.discount*(
                                self.values[ss] if inplace
                                else old_values[ss]
                                ))
                        for ss,p in self.mdp.getTransitionStatesAndProbs(s,a)
                    ) for a in possible_actions)
                )
                self.error = max(self.error,abs(v-self.values[s]))


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        if action == "exit":
            return self.mdp.getReward(state,action,"TERMINAL_STATE")
        ss_and_ps = self.mdp.getTransitionStatesAndProbs(state,action)
        return sum(
            (p * (self.values[ss] * self.discount)
            for ss,p in ss_and_ps)
        )
        return ret

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        possible_actions = self.mdp.getPossibleActions(state)
        if len(possible_actions) <= 0:
            return None
        return sorted(
            ((self.computeQValueFromValues(state,a), a)
                for a in possible_actions),
            key=lambda x:x[0],
            reverse=True
        )[0][1]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
