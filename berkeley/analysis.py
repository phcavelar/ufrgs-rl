# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

# Aluno: 286120

def question2():
    """If there is no risk in crossing the bridge and
    the discount isn't too high, the larger reawrd will be preferred
    """
    answerDiscount = 0.9
    answerNoise = 0.0
    return answerDiscount, answerNoise

def question3a():
    """ Discount is so high that the longer path isn't worth it"""
    answerDiscount = 0.1
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    """Discount is so high that the longer path isn't worth it, but
    there is noise during training and a reward for living,
    such that the bridge is avoided.
    """
    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    """ Discount is low so that the longer path is still worth it
    """
    answerDiscount = 0.9
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    """ Discount is low and there is noise, so that the bridge is avoided
    but the larger reward is preferred.
    """
    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    """ Reward for living is higher than any of the terminal states"""
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 11
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    """ The Reward is either need too many episodes being propagated correctly,
    which is hard for a low epsilon, or a high enough number of episodes that
    exploit it are too few, which is too hard for a high epsilon 
    """
    answerEpsilon = None
    answerLearningRate = None
    return "NOT POSSIBLE" #answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
