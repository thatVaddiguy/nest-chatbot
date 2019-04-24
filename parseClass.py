"""This is a class for parsing sentences.  It is invoked by a test
that specifies the (regular) language to parse.  The
language is specfied by specifying the actual sentences and words.
This builds the topology, and gives an interface for interacting
with it via pynn.

This works by putting sentences in.  It uses these to build up a set
of parse states.  If they have different heads, you call
addSentenceStates, which will build a FSA parser.

"""


#---- Code
from stateMachineClass import FSAHelperFunctions

import os.path

class ParseClass:

    NUMBER_WORDS = 0
    NUMBER_STATES = 0
    wordList = []
    startState = 0
    stateTransitions = []
    wordTransitions = []

    def __init__(self, simName,sim,neal,spinnVersion):
        self.simName = simName
        self.sim = sim
        self.neal = neal
        self.spinnVersion = spinnVersion
        self.simulator = simName
        self.fsa = FSAHelperFunctions(simName,sim,neal,spinnVersion)
        self.fsa.initParams()

    def addWord(self,word):
        if (not(word in self.wordList)):
            self.wordList.append(word)
            self.NUMBER_WORDS += 1

    def getWordNumber(self,word):
        result = self.wordList.index(word)
        return result

    def printWords(self):
        print "Words"
        for word in self.wordList:
            print word

    def addState(self):
        self.NUMBER_STATES += 1
        return self.NUMBER_STATES

    def addTransition(self,startState,finishState):
        self.stateTransitions.append((startState,finishState))

    def printStateTransitions(self):
        print "state transitions"
        for transition in self.stateTransitions:
            print transition

    def addTransitionOnWord(self,word,finishState):
        self.wordTransitions.append((word,finishState))

    def printWordTransitions(self):
        print "word transitions"
        for transition in self.wordTransitions:
            print transition


    def addSentence(self, words):
        for word in words:
            self.addWord(word)
            #print word

    def addSentenceAndStates(self, words):
        currentState = self.startState
        for word in words:
            self.addWord(word)
            nextState = self.addState()
            self.addTransition(currentState,nextState)
            self.addTransitionOnWord(word,nextState)
            currentState = nextState
        return currentState

    #create a new state, and set up the transistions fromState toState and
    #word toState
    def addStateToNewStateOnWord(self, fromState,word):
        toState = self.addState()
        self.addTransition(fromState,toState)
        self.addTransitionOnWord(word,toState)
        return toState

    #create the neurons for the words and the states.
    def createNeurons(self):
        self.NUMBER_STATES += 1 #to account for the start state
        numberWordCells = self.NUMBER_WORDS * self.fsa.CA_SIZE
        numberStateCells = self.NUMBER_STATES * self.fsa.CA_SIZE
        self.stateCells=self.sim.Population(numberStateCells,self.sim.IF_cond_exp,
                    self.fsa.CELL_PARAMS)
        self.wordCells=self.sim.Population(numberWordCells,self.sim.IF_cond_exp,
                    self.fsa.CELL_PARAMS)

    def recordNeurons(self):
        if  (self.simName == 'nest'):
            self.stateCells.record({'spikes','v'})
            self.wordCells.record({'spikes','v'})
        elif  (self.simName == 'spinnaker'):
            if (self.spinnVersion == 7.0):
                self.stateCells.record()
                self.wordCells.record()
            elif (self.spinnVersion == 8.0):
                self.stateCells.record({'spikes','v'})
                self.wordCells.record({'spikes','v'})

    def createCAs(self):
        for wordNumber  in range (0,self.NUMBER_WORDS):
            self.fsa.makeCA(self.wordCells,wordNumber)
        for stateNumber  in range (0,self.NUMBER_STATES):
            self.fsa.makeCA(self.stateCells,stateNumber)

    def createTransitionSynapses(self):
        for stateTransition in self.stateTransitions:
            fromState = stateTransition[0]
            toState = stateTransition[1]
            self.fsa.stateHalfTurnsOnState(self.stateCells,fromState,
                                       self.stateCells,toState)
            self.fsa.stateTurnsOffState(self.stateCells,toState,self.stateCells,
                                    fromState)

        for wordTransition in self.wordTransitions:
            word = wordTransition[0]
            fromState = self.getWordNumber(word)
            toState = wordTransition[1]
            self.fsa.stateHalfTurnsOnState(self.wordCells,fromState,
                                       self.stateCells,toState)
            self.fsa.stateTurnsOffState(self.stateCells,toState,self.wordCells,
                                    fromState)


    def printResults(self):
        if (self.simName == 'nest'):
            self.stateCells.write_data('results/parseState.pkl','spikes')
            #self.stateCells.write_data('results/parseStateV.pkl','v')
            self.wordCells.write_data('results/parseWord.pkl','spikes')
        elif  (self.simName == 'spinnaker'):
            if (self.spinnVersion == 7.0):
                self.stateCells.printSpikes('results/parseState.sp')
                self.wordCells.printSpikes('results/parseWord.sp')
            elif (self.spinnVersion == 8.0):
                self.stateCells.write_data('results/parseState.pkl','spikes')
                self.wordCells.write_data('results/parseWord.pkl','spikes')

    #-- Runtime Interface functions
    def allocateSpinnakerInputs(self):
        import spynnaker_external_devices_plugin.pyNN as externaldevices

        self.InputWordSource= self.sim.Population(
            self.NUMBER_WORDS+1, #for the start
            externaldevices.SpikeInjector,
            {'port': 12345}, label="wordSpikeToBoard")
        externaldevices.activate_live_output_for(self.InputWordSource,
                    database_notify_port_num=12345)

    def connectSpinnakerInputsToWords(self):
        #Each input is connected to its word
        for wordNumber in range (0, self.NUMBER_WORDS):
            self.fsa.oneNeuronTurnsOnState(self.InputWordSource,wordNumber,
                                           self.wordCells,wordNumber)
        #This connects the start state
        self.fsa.oneNeuronTurnsOnState(self.InputWordSource,self.NUMBER_WORDS,
                                           self.stateCells,0)
        print "bob" , self. NUMBER_WORDS+1

    def stopAllStates(self,spikeGenerator):
        for state in range (0,self.NUMBER_STATES):
            self.fsa.turnOffStateFromSpikeSource(spikeGenerator,self.stateCells,
                                                 state)

    #fire the word neurons for a particular nby setting their voltage
    def setCellVoltage(self,CANumber,totalCAs):
        cellVoltages = []
        for CAOffset in range (0,totalCAs):
            for neuronInCA in range (0,self.fsa.CA_SIZE):
                cellVoltages = cellVoltages + [-65.0]

        for neuronInCA in range (0,(self.fsa.CA_SIZE - self.fsa.CA_INHIBS)):
            neuronNumber = (CANumber*self.fsa.CA_SIZE) + neuronInCA
            cellVoltages[neuronNumber] = -30.0

        return cellVoltages

    #typically, a final parse state will turn on an action neuron
    def parseStateStartsNeuron(self,parseState,cellsToActivate,cellNumber):
        self.fsa.stateTurnsOnOneNeuron(self.stateCells,parseState,
                                       cellsToActivate,cellNumber)

    def neuronStopsParseState(self,fromCells,cellNumber,parseState):
        self.fsa.oneNeuronTurnsOffState(fromCells,cellNumber,self.stateCells,
                                         parseState)

    #We get the neuron to spike, by explicitly changing its voltage.
    def setNestInputs(self,time):
        if (not os.path.isfile("words.txt")):
            return
        print "ne file"
        fileHandle = open("words.txt",'r')
        for inpLine in fileHandle:
            splitInp = inpLine.split()
            inpTime = int(splitInp[0])
            wordNumber = int(splitInp[1])
            #You want it to come in the 30ms step window
            if ((inpTime <= time) and ((inpTime+30) > time)):
                print wordNumber
                if (wordNumber == -1):
                    stateVoltages = self.setCellVoltage(0,self.NUMBER_STATES)
                    self.stateCells.initialize(v=stateVoltages)
                else:
                    wordVoltages = self.setCellVoltage(wordNumber,
                                                       self.NUMBER_WORDS)
                    self.wordCells.initialize(v=wordVoltages)

        return
        if ((inpTime <= 100.0) and ((inpTime+30) > 100.0)):
            stateVoltages = self.setCellVoltage(0,self.NUMBER_STATES)
            self.stateCells.initialize(v=stateVoltages)
        elif ((inpTime <= 200.0) and ((inpTime+30) > 200.0)):
            wordVoltages = self.setCellVoltage(0,self.NUMBER_WORDS)
            self.wordCells.initialize(v=wordVoltages)
        elif ((inpTime <= 300.0) and ((inpTime+30) > 300.0)):
            wordVoltages = self.setCellVoltage(1,self.NUMBER_WORDS)
            self.wordCells.initialize(v=wordVoltages)
        elif ((inpTime <= 400.0) and ((inpTime+30) > 400.0)):
            wordVoltages = self.setCellVoltage(2,self.NUMBER_WORDS)
            self.wordCells.initialize(v=wordVoltages)
        return



    #-- Test Functions
    def testTurnOnState(self, state, spikeGenerator):
        #self.fsa.turnOnStateSpikeSource(spikeGenerator,state,self.stateCells)
        self.fsa.turnOnStateFromSpikeSource(spikeGenerator,self.stateCells,state)

    def testTurnOnWord(self, word, spikeGenerator):
        wordNumber = self.getWordNumber(word)
        self.fsa.turnOnStateFromSpikeSource(spikeGenerator,self.wordCells,
                                            wordNumber)


"""
    def printPklSpikes(self,fileName):
        fileHandle = open(fileName)
        neoObj = pickle.load(fileHandle)
        segments = neoObj.segments
        segment = segments[0]
        spikeTrains = segment.spiketrains
        neurons = len(spikeTrains)
        for neuronNum in range (0,neurons):
            if (len(spikeTrains[neuronNum])>0):
                spikes = spikeTrains[neuronNum]
                for spike in range (0,len(spikes)):
                    print neuronNum, spikes[spike]
        fileHandle.close()


    #-----functions called externally and their subfunctions
    def createParseInputs(self):
        if self.simulator == 'nest':
            self.allocateNestInputs()
        elif self.simulator == 'spinnaker':
            self.allocateSpinnakerInputs()


    def connectInputsToWordsAndFirstState(self):
        #set up the input to turn on the first state.
        self.fsa.turnOnStateFromOneNeuron(self.InputWordSource,
                                          self.NUMBER_WORDS,self.stateCells,0)
        for wordNumber  in range (0,self.NUMBER_WORDS):
            self.fsa.turnOnStateFromOneNeuron(self.InputWordSource,wordNumber,
                                              self.wordCells,wordNumber)

    def allocateNestInputs(self):
        if (self.simulator != 'nest'):
            print "Error nest code should be called here"
        numNeurons=self.NUMBER_WORDS+3
        #self.InputWordSource = sim.Create("iaf_cond_exp",
        #            n=self.NUMBER_WORDS+3,params = self.fsa.CELL_PARAMS)
        self.InputWordSource = sim.Population(numNeurons,sim.IF_cond_exp,
                                              self.fsa.CELL_PARAMS)



    #---create inputs for spinnaker spike server
    def allocateSpinnakerInputs(self):
        if self.simulator != 'spinnaker':
            print "Error spinnaker code should be called here"

        self.InputWordSource= sim.Population(self.NUMBER_WORDS+3, #undone +1?
                    externaldevices.SpikeInjector,
                    {'port': 12345}, label="wordSpikeToBoard")
        externaldevices.activate_live_output_for(self.InputWordSource,
                    database_notify_port_num=12345)


    def recordSpinnakerInputs(self):
        #undone this fails because you can't record these.
        if self.simulator != 'spinnaker':
            print "Error spinnaker code should not be called here"
        self.InputWordSource.record()

    def printInputs(self):
        if self.simulator == "nest":
            print "undone***"
            return
            spikes = nest.GetStatus(self.stateSpikeDet)
            stateSpikes = spikes[0]['events']['times']
            print 'State Spikes', stateSpikes
            spikes = nest.GetStatus(self.wordSpikeDet)
            wordSpikes = spikes[0]['events']['times']
            print 'Word Spikes', wordSpikes
        elif self.simulator == 'spinnaker':
            self.InputWordSource.printSpikes('parseInputs.sp')

#-- Access Functions
    def getStateCells(self):
        return self.stateCells

"""
