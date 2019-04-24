""" 
Using the parseClass, build a topology that speficies a parser to parse
these sentences.  

CABot3 Sentences
Turn left.
Turn right.
Turn toward the pyramid.
Turn toward the stalactite.
Move forward. 
Move back. (5)
Move left. 
Move right.
Move before the red stalactite.
Move before the blue stalactite.
Move before the red pyramid.  (10)
Move before the blue pyramid.
Go to the pyramid.
Go to the stalactite.
Go to the door.
Go to the red pyramid.  (15)
Go to the red stalactite.
Go to the blue pyramid.
Go to the blue stalactite.
Centre the pyramid. 
Centre the stalactite.  (20)
Explore. 
Stop. 
"""

import sys

from parseClass import ParseClass

totalSentences = -1#set explicitly
lengthOfLongestSentence = -1 #set explicitly
neal = None
sim = None
simName = None
spinnVersion = None

def addTurnSentences(parser):
    parser.addSentence(['turn','left','.'])
    turnState = parser.addState()
    parser.addTransition(parser.startState,turnState)
    parser.addTransitionOnWord('turn',turnState)
    turnLeftState = parser.addState()
    parser.addTransition(turnState,turnLeftState)
    parser.addTransitionOnWord('left',turnLeftState)
    tLPFinalState = parser.addState()
    parser.addTransition(turnLeftState,tLPFinalState)
    parser.addTransitionOnWord('.',tLPFinalState)

    parser.addSentence(['turn','right','.'])
    turnRightState = parser.addState()
    parser.addTransition(turnState,turnRightState)
    parser.addTransitionOnWord('right',turnRightState)
    tRPFinalState = parser.addState()
    parser.addTransition(turnRightState,tRPFinalState)
    parser.addTransitionOnWord('.',tRPFinalState)

    parser.addSentence(['turn','toward','the','pyramid','.'])
    turnTowardState = parser.addState()
    parser.addTransition(turnState,turnTowardState)
    parser.addTransitionOnWord('toward',turnTowardState)
    turnTowardTheState = parser.addState()
    parser.addTransition(turnTowardState,turnTowardTheState)
    parser.addTransitionOnWord('the',turnTowardTheState)
    turnTowardThePyramidState = parser.addState()
    parser.addTransition(turnTowardTheState,turnTowardThePyramidState)
    parser.addTransitionOnWord('pyramid',turnTowardThePyramidState)
    tttPFinalState = parser.addState()
    parser.addTransition(turnTowardThePyramidState,tttPFinalState)
    parser.addTransitionOnWord('.',tttPFinalState)

    parser.addSentence(['turn','toward','the','stalactite','.'])
    turnTowardTheStalactiteState = parser.addState()
    parser.addTransition(turnTowardTheState,turnTowardTheStalactiteState)
    parser.addTransitionOnWord('stalactite',turnTowardTheStalactiteState)
    tttSFinalState = parser.addState()
    parser.addTransition(turnTowardTheStalactiteState,tttSFinalState)
    parser.addTransitionOnWord('.',tttSFinalState)

    return [tLPFinalState,tRPFinalState,tttPFinalState,tttSFinalState]

def addCentreSentences(parser):
    parser.addSentence(['centre','the','pyramid','.'])
    centreState = parser.addStateToNewStateOnWord(parser.startState,'centre')
    centreTheState = parser.addStateToNewStateOnWord(centreState,'the')
    centreThePState = parser.addStateToNewStateOnWord(centreTheState,'pyramid')
    ctpFinalState = parser.addStateToNewStateOnWord(centreThePState,'.')

    parser.addSentence(['centre','the','stalactite','.'])
    centreTheSState = parser.addStateToNewStateOnWord(centreTheState,
                                                      'stalactite')
    ctsFinalState = parser.addStateToNewStateOnWord(centreTheSState,'.')

    return [ctpFinalState,ctsFinalState]


def addMoveSentences(parser):
    global lengthOfLongestSentence 
    parser.addSentence(['move','forward','.']) 
    moveState = parser.addStateToNewStateOnWord(parser.startState,'move')
    moveForwardState = parser.addStateToNewStateOnWord(moveState,'forward')
    mfFinalState = parser.addStateToNewStateOnWord(moveForwardState,'.')

    parser.addSentence(['move','back','.']) 
    moveBackState = parser.addStateToNewStateOnWord(moveState,'back')
    mbFinalState = parser.addStateToNewStateOnWord(moveBackState,'.')

    parser.addSentence(['move','left','.']) 
    moveLeftState = parser.addStateToNewStateOnWord(moveState,'left')
    mlFinalState = parser.addStateToNewStateOnWord(moveLeftState,'.')

    parser.addSentence(['move','right','.']) 
    moveRightState = parser.addStateToNewStateOnWord(moveState,'right')
    mrFinalState = parser.addStateToNewStateOnWord(moveRightState,'.')

    parser.addSentence(['move','before','the','red','stalactite','.']) 
    lengthOfLongestSentence = 6

    moveBeforeState = parser.addStateToNewStateOnWord(moveState,'before')
    moveBeforeTState = parser.addStateToNewStateOnWord(moveBeforeState,'the')
    moveBeforeTRState = parser.addStateToNewStateOnWord(moveBeforeTState,'red')
    moveBeforeTRSState = parser.addStateToNewStateOnWord(moveBeforeTRState,
                                                         'stalactite')
    mbtrsFinalState = parser.addStateToNewStateOnWord(moveBeforeTRSState,'.')


    parser.addSentence(['move','before','the','blue','stalactite','.']) 
    moveBeforeTBState = parser.addStateToNewStateOnWord(moveBeforeTState,'blue')
    moveBeforeTBSState = parser.addStateToNewStateOnWord(moveBeforeTBState,
                                                         'stalactite')
    mbtbsFinalState = parser.addStateToNewStateOnWord(moveBeforeTBSState,'.')

    parser.addSentence(['move','before','the','red','pyramid','.']) 
    moveBeforeTRPState = parser.addStateToNewStateOnWord(moveBeforeTRState,
                                                         'pyramid')
    mbtrpFinalState = parser.addStateToNewStateOnWord(moveBeforeTRPState,'.')

    parser.addSentence(['move','before','the','blue','pyramid','.']) 
    moveBeforeTBPState = parser.addStateToNewStateOnWord(moveBeforeTBState,
                                                         'pyramid')
    mbtbpFinalState = parser.addStateToNewStateOnWord(moveBeforeTBPState,'.')

    return [mfFinalState,mbFinalState,mlFinalState,mrFinalState,mbtrsFinalState, mbtbsFinalState,mbtrpFinalState,mbtbpFinalState]

def addGoSentences(parser):
    parser.addSentence(['go','to','the', 'pyramid','.']) 
    goState = parser.addStateToNewStateOnWord(parser.startState,'go')
    goToState = parser.addStateToNewStateOnWord(goState,'to')
    goToTheState = parser.addStateToNewStateOnWord(goToState,'the')
    goToThePState = parser.addStateToNewStateOnWord(goToTheState,'pyramid')
    gttpFinalState = parser.addStateToNewStateOnWord(goToThePState,'.')

    parser.addSentence(['go','to','the', 'stalactite','.']) 
    goToTheSState = parser.addStateToNewStateOnWord(goToTheState,'stalactite')
    gttsFinalState = parser.addStateToNewStateOnWord(goToTheSState,'.')

    parser.addSentence(['go','to','the', 'door','.']) 
    goToTheDState = parser.addStateToNewStateOnWord(goToTheState,'door')
    gttdFinalState = parser.addStateToNewStateOnWord(goToTheDState,'.')

    parser.addSentence(['go','to','the', 'red','pyramid','.']) 
    goToTheRState = parser.addStateToNewStateOnWord(goToTheState,'red')
    goToTheRPState = parser.addStateToNewStateOnWord(goToTheRState,'pyramid')
    gttrpFinalState = parser.addStateToNewStateOnWord(goToTheRPState,'.')

    parser.addSentence(['go','to','the', 'red','stalactite','.']) 
    goToTheRSState = parser.addStateToNewStateOnWord(goToTheRState,'stalactite')
    gttrsFinalState = parser.addStateToNewStateOnWord(goToTheRSState,'.')

    parser.addSentence(['go','to','the', 'blue','pyramid','.']) 
    goToTheBState = parser.addStateToNewStateOnWord(goToTheState,'blue')
    goToTheBPState = parser.addStateToNewStateOnWord(goToTheBState,'pyramid')
    gttbpFinalState = parser.addStateToNewStateOnWord(goToTheBPState,'.')

    parser.addSentence(['go','to','the', 'blue','stalactite','.']) 
    goToTheBSState = parser.addStateToNewStateOnWord(goToTheBState,'stalactite')
    gttbsFinalState = parser.addStateToNewStateOnWord(goToTheBSState,'.')

    return [gttpFinalState,gttsFinalState,gttdFinalState,gttrpFinalState,gttrsFinalState,gttbpFinalState,gttbsFinalState]

def linkInSink(spikeSource,sinkCell):
    global simName
    global neal
    if (simName == 'spinnaker'):
        connector = [(0,0,1.0, neal.DELAY)]
        neal.nealProjection(spikeSource,sinkCell,connector,'inhibitory') 

#spinnaker crashes if a spike source isn't connected to
#something.  Make the something here.
def allocateSinks(firstSink,spikeGenerators):
    global simName
    global sim
    if (simName != 'spinnaker'):
        return
    sinkCell=sim.Population(1,sim.IF_cond_exp,{})
    for sinkNumber  in range (firstSink,7):
        linkInSink(spikeGenerators[sinkNumber],sinkCell)

def setupTestSentences(parser,spikeGenerators,sentence):
    if (sentence == 0):
        parser.testTurnOnWord("turn",spikeGenerators[1])
        parser.testTurnOnWord("left",spikeGenerators[2])
        parser.testTurnOnWord(".",spikeGenerators[3])
        allocateSinks(4,spikeGenerators)
    elif (sentence == 1):
        parser.testTurnOnWord("turn",spikeGenerators[1])
        parser.testTurnOnWord("right",spikeGenerators[2])
        parser.testTurnOnWord(".",spikeGenerators[3])
        allocateSinks(4,spikeGenerators)
    elif (sentence == 2):
        parser.testTurnOnWord("turn",spikeGenerators[1])
        parser.testTurnOnWord("toward",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("pyramid",spikeGenerators[4])
        parser.testTurnOnWord(".",spikeGenerators[5])
        allocateSinks(6,spikeGenerators)
    elif (sentence == 3):
        parser.testTurnOnWord("turn",spikeGenerators[1])
        parser.testTurnOnWord("toward",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("stalactite",spikeGenerators[4])
        parser.testTurnOnWord(".",spikeGenerators[5])
        allocateSinks(6,spikeGenerators)
    elif (sentence == 4):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("forward",spikeGenerators[2])
        parser.testTurnOnWord(".",spikeGenerators[3])
        allocateSinks(4,spikeGenerators)
    elif (sentence == 5):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("back",spikeGenerators[2])
        parser.testTurnOnWord(".",spikeGenerators[3])
        allocateSinks(4,spikeGenerators)
    elif (sentence == 6):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("left",spikeGenerators[2])
        parser.testTurnOnWord(".",spikeGenerators[3])
        allocateSinks(4,spikeGenerators)
    elif (sentence == 7):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("right",spikeGenerators[2])
        parser.testTurnOnWord(".",spikeGenerators[3])
        allocateSinks(4,spikeGenerators)
    elif (sentence == 8):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("before",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("red",spikeGenerators[4])
        parser.testTurnOnWord("stalactite",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 9):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("before",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("blue",spikeGenerators[4])
        parser.testTurnOnWord("stalactite",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 10):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("before",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("red",spikeGenerators[4])
        parser.testTurnOnWord("pyramid",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 11):
        parser.testTurnOnWord("move",spikeGenerators[1])
        parser.testTurnOnWord("before",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("blue",spikeGenerators[4])
        parser.testTurnOnWord("pyramid",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 12):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("pyramid",spikeGenerators[4])
        parser.testTurnOnWord(".",spikeGenerators[5])
        allocateSinks(6,spikeGenerators)
    elif (sentence == 13):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("stalactite",spikeGenerators[4])
        parser.testTurnOnWord(".",spikeGenerators[5])
        allocateSinks(6,spikeGenerators)
    elif (sentence == 14):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("door",spikeGenerators[4])
        parser.testTurnOnWord(".",spikeGenerators[5])
        allocateSinks(6,spikeGenerators)
    elif (sentence == 15):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("red",spikeGenerators[4])
        parser.testTurnOnWord("pyramid",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 16):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("red",spikeGenerators[4])
        parser.testTurnOnWord("stalactite",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 17):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("blue",spikeGenerators[4])
        parser.testTurnOnWord("pyramid",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 18):
        parser.testTurnOnWord("go",spikeGenerators[1])
        parser.testTurnOnWord("to",spikeGenerators[2])
        parser.testTurnOnWord("the",spikeGenerators[3])
        parser.testTurnOnWord("blue",spikeGenerators[4])
        parser.testTurnOnWord("stalactite",spikeGenerators[5])
        parser.testTurnOnWord(".",spikeGenerators[6])
    elif (sentence == 19):
        parser.testTurnOnWord("centre",spikeGenerators[1])
        parser.testTurnOnWord("the",spikeGenerators[2])
        parser.testTurnOnWord("pyramid",spikeGenerators[3])
        parser.testTurnOnWord(".",spikeGenerators[4])
        allocateSinks(5,spikeGenerators)
    elif (sentence == 20):
        parser.testTurnOnWord("centre",spikeGenerators[1])
        parser.testTurnOnWord("the",spikeGenerators[2])
        parser.testTurnOnWord("stalactite",spikeGenerators[3])
        parser.testTurnOnWord(".",spikeGenerators[4])
        allocateSinks(5,spikeGenerators)
    elif (sentence == 21):
        parser.testTurnOnWord("explore",spikeGenerators[1])
        parser.testTurnOnWord(".",spikeGenerators[2])
        allocateSinks(3,spikeGenerators)
    elif (sentence == 22):
        parser.testTurnOnWord("stop",spikeGenerators[1])
        parser.testTurnOnWord(".",spikeGenerators[2])
        allocateSinks(3,spikeGenerators)

#access functions for variables from this file
def getTotalSentences():
    return totalSentences

def getLengthOfLongestSentence():
    return lengthOfLongestSentence


#---main 
def main(simNameInput,simInput,nealInput,spinnVersionInput):
    global neal
    global sim
    global simName
    global spinnVersion

    global totalSentences
    #allocate neal and a parser
    neal = nealInput
    sim = simInput
    simName = simNameInput
    spinnVersion = spinnVersionInput

    parser = ParseClass(simName,sim,neal,spinnVersion)

    #specify the sentences you want to parse.
    tFinalStates = addTurnSentences(parser)
    mFinalStates = addMoveSentences(parser)
    gFinalStates = addGoSentences(parser)
    cFinalStates = addCentreSentences(parser)

    eFinalState = parser.addSentenceAndStates(['explore','.']) 
    sFinalState = parser.addSentenceAndStates(['stop','.']) 
    totalSentences = 23

    #optionally, print out information about the parser
    #parser.printWords()
    #parser.printStateTransitions()
    #parser.printWordTransitions()

    print "Final states in order"
    print tFinalStates,mFinalStates,gFinalStates,cFinalStates,eFinalState,sFinalState

    #allocate the topology
    parser.createNeurons()
    parser.recordNeurons()
    parser.createCAs()
    parser.createTransitionSynapses()

    #access the topology via the parser
    return parser



