"""
Using the parseClass, build a topology that speficies a parser to parse
these sentences.

turn step  Sentences
Turn left.
Step forward.
"""

import sys

from parseClass import ParseClass

totalSentences = -1#set explicitly
lengthOfLongestSentence = -1 #set explicitly
neal = None
sim = None
simName = None
spinnVersion = None

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
    sinkCell=sim.Population(1,sim.IF_cond_exp,{})
    for sinkNumber  in range (firstSink,7):
        linkInSink(spikeGenerators[sinkNumber],sinkCell)

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
    global lengthOfLongestSentence

    #allocate neal and a parser
    neal = nealInput
    sim = simInput
    simName = simNameInput
    spinnVersion = spinnVersionInput
    parser = ParseClass(simName,sim,neal,spinnVersion)

    #making the language for the parser
    #adding the add sentences to the parser
    addStateNum = []
    parser.addSentence(['add','bulb','.'])
    addAddState = parser.addStateToNewStateOnWord(parser.startState,'add') #0
    addBulbState = parser.addStateToNewStateOnWord(addAddState,'bulb') #1
    addBulbFinalState = parser.addStateToNewStateOnWord(addBulbState,'.') #2
    addStateNum.append(addBulbFinalState)
    parser.addSentence(['add','fan','.'])
    addFanState = parser.addStateToNewStateOnWord(addAddState,'fan') #3
    addFanFinalState = parser.addStateToNewStateOnWord(addFanState,'.') #4
    addStateNum.append(addFanFinalState)
    parser.addSentence(['add','music','.'])
    addMusicState = parser.addStateToNewStateOnWord(addAddState,'music') #5
    addMusicFinalState = parser.addStateToNewStateOnWord(addMusicState,'.') #6
    addStateNum.append(addMusicFinalState)
    parser.addSentence(['add','tv','.'])
    addTvState = parser.addStateToNewStateOnWord(addAddState,'tv') #7
    addTvFinalState = parser.addStateToNewStateOnWord(addTvState,'.') #8
    addStateNum.append(addTvFinalState)
    parser.addSentence(['add','thermostat','.'])
    addThermoState = parser.addStateToNewStateOnWord(addAddState,'thermostat') #9
    addThermoFinalState = parser.addStateToNewStateOnWord(addThermoState,'.') #10
    addStateNum.append(addThermoFinalState)

    #adding the turn on sentences to the parser
    onStateNum = []
    parser.addSentence(['turn','on','bulb','.'])
    turnState = parser.addStateToNewStateOnWord(parser.startState,'turn') #11
    turnOnState = parser.addStateToNewStateOnWord(turnState,'on') #12
    turnOnBulbState = parser.addStateToNewStateOnWord(turnOnState,'bulb') #13
    turnOnBulbFinalState = parser.addStateToNewStateOnWord(turnOnBulbState,'.') #14
    onStateNum.append(turnOnBulbFinalState)
    parser.addSentence(['turn','on','fan','.'])
    turnOnFanState = parser.addStateToNewStateOnWord(turnOnState,'fan') #15
    turnOnFanFinalState = parser.addStateToNewStateOnWord(turnOnFanState,'.') #16
    onStateNum.append(turnOnFanFinalState)
    parser.addSentence(['turn','on','tv','.'])
    turnOnTvState = parser.addStateToNewStateOnWord(turnOnState,'tv') #17
    turnOnTvFinalState = parser.addStateToNewStateOnWord(turnOnTvState,'.') #18
    onStateNum.append(turnOnTvFinalState)
    parser.addSentence(['turn','on','music','.'])
    turnOnMusicState = parser.addStateToNewStateOnWord(turnOnState,'music') #19
    turnOnMusicFinalState = parser.addStateToNewStateOnWord(turnOnMusicState,'.') #20
    onStateNum.append(turnOnMusicFinalState)

    #adding the turn off sentences to the parser
    offStateNum = []
    parser.addSentence(['turn','off','bulb','.'])
    turnOffState = parser.addStateToNewStateOnWord(turnState,'off') #21
    turnOffBulbState = parser.addStateToNewStateOnWord(turnOffState,'bulb') #22
    turnOffBulbFinalState = parser.addStateToNewStateOnWord(turnOffBulbState,'.') #23
    offStateNum.append(turnOffBulbFinalState)
    parser.addSentence(['turn','off','fan','.'])
    turnOffFanState = parser.addStateToNewStateOnWord(turnOffState,'fan') #24
    turnOffFanFinalState = parser.addStateToNewStateOnWord(turnOffFanState,'.') #25
    offStateNum.append(turnOffFanFinalState)
    parser.addSentence(['turn','off','tv','.'])
    turnOffTvState = parser.addStateToNewStateOnWord(turnOffState,'tv') #26
    turnOffTvFinalState = parser.addStateToNewStateOnWord(turnOffTvState,'.') #27
    offStateNum.append(turnOffTvFinalState)
    parser.addSentence(['turn','off','music','.'])
    turnOffMusicState = parser.addStateToNewStateOnWord(turnOffState,'music') #28
    turnOffMusicFinalState = parser.addStateToNewStateOnWord(turnOffMusicState,'.') #29
    offStateNum.append(turnOffMusicFinalState)

    #adding the set thermostat sentences to the parser
    thermoStateNum = []
    parser.addSentence(['set','thermostat','low','.'])
    setState = parser.addStateToNewStateOnWord(parser.startState,'set') #30
    setThermoState = parser.addStateToNewStateOnWord(setState,'thermostat') #31
    setThermoLowState = parser.addStateToNewStateOnWord(setThermoState,'low') #32
    setThermoLowFinalState = parser.addStateToNewStateOnWord(setThermoLowState,'.') #33
    thermoStateNum.append(setThermoLowFinalState)
    parser.addSentence(['set','thermostat','mid','.'])
    setThermoMidState = parser.addStateToNewStateOnWord(setThermoState,'mid') #34
    setThermoMidFinalState = parser.addStateToNewStateOnWord(setThermoMidState,'.') #35
    thermoStateNum.append(setThermoMidFinalState)
    parser.addSentence(['set','thermostat','high','.'])
    setThermoHighState = parser.addStateToNewStateOnWord(setThermoState,'high') #36
    setThermoHighFinalState = parser.addStateToNewStateOnWord(setThermoHighState,'.') #37
    thermoStateNum.append(setThermoHighFinalState)


    totalSentences = 16
    lengthOfLongestSentence = 3

    #optionally, print out information about the parser
    parser.printWords()
    #parser.printStateTransitions()
    #parser.printWordTransitions()

    #printing the final states of the sentences
    print "Final states in order"
    print addStateNum, onStateNum, offStateNum, thermoStateNum

    #allocate the topology
    parser.createNeurons()
    parser.recordNeurons()
    parser.createCAs()
    parser.createTransitionSynapses()

    #access the topology via the parser
    return parser
