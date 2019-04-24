"""
The environment connects with nest via files (words.txt and actions.txt).
It connects with spinnaker via eieio.
"""

import sys

import time as t
popsLoadedOnBoard = False

#slow environment down by factor of 10
environmentSpeed = 10 

def canSend(label, sender):
        print_condition.acquire()
        print "can Send crh",sender, spikeQueue.popsLoadedOnBoard
        print_condition.release()
        spikeQueue.popsLoadedOnBoard = spikeQueue.popsLoadedOnBoard -1
        

def gotInput(label, time, sender):
        #ignore extra commands
        if (spikeQueue.fHaveCommandFromBoard):
                if (label < 4):
                        print "ignore Input",label,time,sender
                        return
        print "got Input",label,time,sender
        neuron_id = sender[0]
        spikeQueue.setCommandFromBoard(neuron_id)

def gotClockInput(label, time, sender):
        #print "got Clock Input",label,time,sender
        neuron_id = sender[0]
        spikeQueue.spinnSetTicks(time)

class spikeQueue:
    def __init__(self):
        print "new q"
        self.timesToSend = 2 #use this to get a finite number of input cycles.
                             #Need to comment back in in writeBWPicture
        self.timeTicks = 0
        print "hey nest"

        #init sentence variables
        self.currentSentenceLeft = 0
        self.currentPosInSent = 0

    #for nest only
    def setTicks(self,newTicks):
            self.timeTicks = newTicks

    #for nest only
    def getTicks(self):
        return self.timeTicks

    def sendWord(self):
        global popsLoadedOnBoard
        if not popsLoadedOnBoard:
                return
        if self.currentSentenceLeft == 0:
            return

        print "sw ", self.currentSentence[self.currentPosInSent]
        mess = self.currentSentence[self.currentPosInSent]
        if (mess == -1):
                mess = 5 #undone this is the last word + 1 to get the state

        if (nealParameters.simulator == "nest"):
                print "hey",self.timeTicks,"error?"
        
        elif (nealParameters.simulator == 'spinnaker'):
                self.spikesToSpinnConn.send_spike("wordSpikeToBoard",
                        mess,send_full_keys=True)

        t.sleep(0.1)

        self.currentPosInSent += 1
        self.currentSentenceLeft -= 1
        return

    def increaseTimeTicks(self):
        self.timeTicks+=environmentSpeed
        print self.timeTicks,"time"
        return

    #Apr16 the nest word writing and io in general is different than
    #the spinnaker.  Here we write the sentence in one go to a file
    #which is read by pynn
    def writeSentence(self,sentence,length):
        print "nest",self.timeTicks,sentence,length
        fileHandle = open("words.txt",'w')
        for wordNumber in range (0,length):
                #round time to 10
                sendTime = self.timeTicks/10
                sendTime = sendTime*10
                print sendTime,(wordNumber*100),sentence[wordNumber]
                outString = str(sendTime+(wordNumber*100))
                outString += " "
                outString += str(sentence[wordNumber])
                outString += "\n"
                fileHandle.write(outString)
                self.currentSentenceLeft = 0

        fileHandle.close()

        print sentence
        if self.currentSentenceLeft == 0:
            self.currentPosInSent = 0
            self.currentSentenceLeft = length
            self.currentSentence = sentence
            print "new sentence sent"
        else:
            print "trying to parse new sentence while parsing", self.currentSentenceLeft,self.currentSentence

