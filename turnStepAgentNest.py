"""

"""

import sys
import time

import pyNN.nest as sim

from nealCoverClass import NealCoverFunctions
from stateMachineClass import FSAHelperFunctions
from parseClass import ParseClass
import turnStepLang as languageToDefine

def init():
    #print "spin" or nest
    sim.setup(timestep=neal.DELAY,
                    min_delay=neal.DELAY,
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


def setNestInput(currentSimulationTime,parser):
    parser.setNestInputs(currentSimulationTime)

def newActionOutput(currentSimulationTime,actionCells):
    output = []
    actionData = actionCells.get_data()
    actionSegments = actionData.segments[0]
    actionSpikeTrains = actionSegments.spiketrains
    for action in range (0,len(actionSpikeTrains)):
        if (len(actionSpikeTrains[action]) > 0):
            anActionsSpikes = actionSpikeTrains[action]
            for spike in range (0,len(anActionsSpikes)):
                aSpike = anActionsSpikes[spike]
                if (aSpike <= currentSimulationTime) and (aSpike > currentSimulationTime-30):
                    output = output + [action]
                    print 'ho', currentSimulationTime,action

    return output

def setNestOutput(currentSimulationTime,plan):
    if (currentSimulationTime == 0):
        nestOutputFileHandle = open("actions.txt",'a')
        nestOutputFileHandle.write(str(currentSimulationTime)+"\n")
        nestOutputFileHandle.close()
        return
    actions = newActionOutput(currentSimulationTime,plan)
    if (len(actions) > 0):
        nestOutputFileHandle = open("actions.txt",'a')
        for actionNum in range (0,len(actions)):
            nestOutputFileHandle.write(str(actions[actionNum])+" "+
                                       str(currentSimulationTime)+"\n")
        nestOutputFileHandle.close()

def runAgent(parser,actionCells):
    callbackTimeStepLength = 30
    steps = int(SIM_LENGTH/callbackTimeStepLength)
    for step in range (0, steps):
        currentTime = step*callbackTimeStepLength
        setNestInput(currentTime,parser)
        setNestOutput(currentTime,actionCells)
        print "nest simulation timestep ", currentTime
        sim.run(callbackTimeStepLength)
        time.sleep(0.7)

def connectFinalParseToAction(parser,parseState,actionCells,actionCellNumber):
    parser.parseStateStartsNeuron(parseState,actionCells, actionCellNumber)
    parser.neuronStopsParseState(actionCells, actionCellNumber,parseState)


#---main
simName = "nest"
spinnVersion = -1
neal = NealCoverFunctions(simName,sim,spinnVersion)
fsa = FSAHelperFunctions(simName,sim,neal,spinnVersion)

SIM_LENGTH = 10000.0

init()

parser = languageToDefine.main(simName,sim,neal,spinnVersion)

agentActionCells = sim.Population(20,sim.IF_cond_exp,{})
agentActionCells.record({'spikes','v'})
agentActionCells.record({'spikes','v'})

#connecting final states of sentences to process commands to send to the gui
connectFinalParseToAction(parser,3,agentActionCells,0)# add bulb
connectFinalParseToAction(parser,5,agentActionCells,1)# add fan
connectFinalParseToAction(parser,7,agentActionCells,2)# add music
connectFinalParseToAction(parser,9,agentActionCells,3)# add tv
connectFinalParseToAction(parser,11,agentActionCells,4)# add thermo
connectFinalParseToAction(parser,15,agentActionCells,5)#turn on bulb
connectFinalParseToAction(parser,17,agentActionCells,6)#turn on fan
connectFinalParseToAction(parser,19,agentActionCells,7)# turn on tv
connectFinalParseToAction(parser,21,agentActionCells,8)# turn on music
connectFinalParseToAction(parser,24,agentActionCells,9)#turn off bulb
connectFinalParseToAction(parser,26,agentActionCells,10)#turn off fan
connectFinalParseToAction(parser,28,agentActionCells,11)# turn off tv
connectFinalParseToAction(parser,30,agentActionCells,12)# turn off music
connectFinalParseToAction(parser,34,agentActionCells,13)# set thermo low
connectFinalParseToAction(parser,36,agentActionCells,14)# set thermo mid
connectFinalParseToAction(parser,38,agentActionCells,15)# set thermo high

neal.nealApplyProjections()
runAgent(parser,agentActionCells)

parser.printResults()
agentActionCells.write_data('results/agentAction.pkl','spikes')

sim.end()
