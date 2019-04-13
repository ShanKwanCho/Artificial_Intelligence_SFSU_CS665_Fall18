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
    def __init__(self, mdp, discount = 0.9, iterations = 100):
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
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
          New_Val = util.Counter()
          for state in mdp.getStates():
              if mdp.isTerminal(state):  #new val of state pass in array with 0 if satisfied terminal state
                 New_Val[state]=0
                 continue;
              Action = mdp.getPossibleActions(state)
              if not Action:
                 New_Val[state]=0
              Max_Value = -float('inf')
              Q_value = 0
              for j in mdp.getPossibleActions(state):
                  Q_value = self.getQValue(state,j);
                  if Q_value > Max_Value:
                      Max_Value = Q_value
                      New_Val[state] = Q_value
          self.values = New_Val


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
        "*** YOUR CODE HERE ***"

        Q_value = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            Q_value += prob * (self.mdp.getReward(state,action,nextState) + self.discount * self.getValue(nextState))
        return Q_value

        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        Max_Action = None
        Max_Reward = float('-inf')

        Action = self.mdp.getPossibleActions(state)
        for action in Action:
          transitions = self.mdp.getTransitionStatesAndProbs(state, action)
          Q_value = self.computeQValueFromValues(state, action)

          if Q_value > Max_Reward:
            Max_Reward = Q_value
            Max_Action = action

        return Max_Action

        #util.raiseNotDefined()


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)