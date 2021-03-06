""" 
This is just to test the cabot3 parser on one sentence.  Call it
python testLangOneSentence.py sentenceNumber, for example
python testLangOneSentence.py 0.

It should generate two files (pkl in nest .sp in spinnaker), that
represent the parse of the sentence in the results directory.
"""


from nealCoverClass import NealCoverFunctions
import pyNN.nest as sim
from stateMachineClass import FSAHelperFunctions

from parseClass import ParseClass
import turnStepLang as languageToDefine

def init():
    #print "spin" or nest
    sim.setup(timestep=neal.DELAY, min_delay=neal.DELAY,
                    max_delay=neal.DELAY, debug=0)

def createInputs(startTime):
    inputSpikeTimes0 = [10.0 + startTime] 
    inputSpikeTimes1 = [50.0 + startTime]
    inputSpikeTimes2 = [100.0 + startTime]
    inputSpikeTimes3 = [150.0 + startTime]
    inputSpikeTimes4 = [200.0 + startTime]
    inputSpikeTimes5 = [250.0 + startTime]
    inputSpikeTimes6 = [300.0 + startTime]
    stopSpikeTimes = [400.0 + startTime]
    
    spikeArray0 = {'spike_times': [inputSpikeTimes0]}
    spikeArray1 = {'spike_times': [inputSpikeTimes1]}
    spikeArray2 = {'spike_times': [inputSpikeTimes2]}
    spikeArray3 = {'spike_times': [inputSpikeTimes3]}
    spikeArray4 = {'spike_times': [inputSpikeTimes4]}
    spikeArray5 = {'spike_times': [inputSpikeTimes5]}
    spikeArray6 = {'spike_times': [inputSpikeTimes6]}
    stopSpikeArray = {'spike_times': [stopSpikeTimes]}
    spikeGen0=sim.Population(1,sim.SpikeSourceArray,spikeArray0,
                                   label='inputSpikes_0')
    spikeGen1=sim.Population(1, sim.SpikeSourceArray, spikeArray1,
                                   label='inputSpikes_1')
    spikeGen2=sim.Population(1, sim.SpikeSourceArray, spikeArray2,
                                   label='inputSpikes_2')
    spikeGen3=sim.Population(1, sim.SpikeSourceArray, spikeArray3,
                                   label='inputSpikes_3')
    spikeGen4=sim.Population(1, sim.SpikeSourceArray, spikeArray4,
                                   label='inputSpikes_4')
    spikeGen5=sim.Population(1, sim.SpikeSourceArray, spikeArray5,
                                   label='inputSpikes_5')
    spikeGen6=sim.Population(1, sim.SpikeSourceArray, spikeArray6,
                                   label='inputSpikes_6')
    stopSpikeGen=sim.Population(1, sim.SpikeSourceArray, stopSpikeArray,
                                   label='stopSpikes')

    return [spikeGen0,spikeGen1,spikeGen2,spikeGen3,spikeGen4,spikeGen5,
            spikeGen6,stopSpikeGen]

def linkInSink(spikeSource,sinkCell):
    if (nealParameters.simulator == 'spinnaker'):
        connector = [(0,0,1.0, nealParameters.DELAY)]
        neal.nealProjection(spikeSource,sinkCell,connector,'inhibitory') 

#spinnaker crashes if a spike source isn't connected to
#something.  Make the something here.
def allocateSinks(firstSink,generators):
    if (nealParameters.simulator != 'spinnaker'):
        return
    sinkCell=sim.Population(1,sim.IF_cond_exp,{})
    for sinkNumber  in range (firstSink,7):
        linkInSink(spikeGenerators[sinkNumber],sinkCell)

#---main 
simName = "nest"
spinnVersion = -1
neal = NealCoverFunctions(simName,sim,spinnVersion)
fsa = FSAHelperFunctions(simName,sim,neal,spinnVersion)

sentenceToParse = 0

init() 
parser = languageToDefine.main(simName,sim,neal,spinnVersion)

#Each sentence has 50ms per word + 50 for the start, 50 for the stop, to
#let the words be processed.
oneSentenceParseTime = 50*(languageToDefine.getLengthOfLongestSentence()+3)
sentenceStartTime = 0

spikeGenerators = createInputs(0.0)
parser.testTurnOnState(0,spikeGenerators[0])
languageToDefine.setupTestSentences(parser,spikeGenerators,sentenceToParse)
parser.stopAllStates(spikeGenerators[7])

fullTestTime = oneSentenceParseTime
print fullTestTime,sentenceToParse

neal.nealApplyProjections()
sim.run(fullTestTime)

parser.printResults()

sim.end()


