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
import collections

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
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        iteration_counter = 0
        states = self.mdp.getStates()
        while iteration_counter < self.iterations:
            dictionary = util.Counter()
            for state in states:
                if not self.mdp.isTerminal(state):
                    optimal_action = self.computeActionFromValues(state)
                    dictionary[state] = self.computeQValueFromValues(state, optimal_action)
            self.values = dictionary
            iteration_counter += 1

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
        QValue = 0
        transitionstates_probs = self.mdp.getTransitionStatesAndProbs(state, action)
        for pair in transitionstates_probs:
            transition_state = pair[0]
            prob = pair[1]
            reward = self.mdp.getReward(state, action, transition_state)
            QValue += prob * (reward + (self.discount * self.values[transition_state]))
        return QValue
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        optimal_action = ""
        optimal_QValue = float("-inf")
        for action in self.mdp.getPossibleActions(state):
            temp_QValue = self.computeQValueFromValues(state, action)
            if  temp_QValue > optimal_QValue:
                optimal_action = action
                optimal_QValue = temp_QValue

        return optimal_action
        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        states_length = len(states)
        iteration_counter = 0
        while iteration_counter < self.iterations:
            state = states[iteration_counter % states_length]
            if not self.mdp.isTerminal(state):
                optimal_action = self.computeActionFromValues(state)
                self.values[state] = self.computeQValueFromValues(state, optimal_action)
            iteration_counter += 1


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessors = {}
        states = self.mdp.getStates()
        #Compute predecessors of all states
        for state in states:
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    transitionstates_probs = self.mdp.getTransitionStatesAndProbs(state, action)
                    for pair in transitionstates_probs:
                        transition_state = pair[0]
                        prob = pair[1]
                        if prob != 0:
                            if transition_state in predecessors:
                                predecessors[transition_state].add(state)
                            else:
                                predecessors[transition_state] = {state}
        #Initialize an empty priority queue
        queue = util.PriorityQueue()
        # For each non terminal state:
        # 1. Find diff
        # 2. Push state into priority queue with priority -diff
        for state in states:
            if not self.mdp.isTerminal(state):
                optimal_action = self.computeActionFromValues(state)
                QValue = self.computeQValueFromValues(state, optimal_action)
                diff = abs(self.values[state] - QValue)
                queue.update(state, -diff)

        # For each iteration......
        iteration_counter = 0
        while iteration_counter < self.iterations:
            if queue.isEmpty():
                return
            s = queue.pop()
            if not self.mdp.isTerminal(s):
                opt_action = self.computeActionFromValues(s)
                Q = self.computeQValueFromValues(s, opt_action)
                self.values[s] = Q
                for p in predecessors[s]:
                    best_action = self.computeActionFromValues(p)
                    best_QValue = self.computeQValueFromValues(p, best_action)
                    difference = abs(self.values[p] - best_QValue)
                    if difference > self.theta:
                        queue.update(p, -difference)
            iteration_counter += 1
