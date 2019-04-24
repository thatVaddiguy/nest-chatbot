"""
This is the nest version of the world.  It's got a text box that you can
put inputs into.  These are then sent to the agent in the form of
spikes, it processes them, and returns an action.  The communication is
done by text files:  words.txt for information from the environment to
the agent; actions.txt for information from the agent to the environment.
"""

import sys
import os.path
from Tkinter import Tk, Canvas, BOTH
from Tkinter import *
from ttk import *

from spikeServeNest import spikeQueue

import math
#import time

class Environment(Frame):

    numFiles = 0
    numUserFiles = 0

    def __init__(self, parent):
        self.fileNum = 0
        Frame.__init__(self, parent)
        self.toSpinQ = spikeQueue() #undone probably should rename

        #set up call back to interact with agent
        self.after(200,self.getNestInput)

        self.parent = parent
        self.initUI()
        # self.loadtable()

    nestInputLines = 0
    #get the actions from the text file created in cabot3X.py
    def getNewNestInput(self,fileHandle):
        lineCount = 0
        for inpLine in fileHandle:
            lineCount += 1
            if (lineCount > self.nestInputLines):
                splitInp = inpLine.split()
                print "get action",inpLine,splitInp
                action = int(splitInp[0])
                fileHandle.close()
                if (splitInp.__len__() > 1):
                    actionTime = int(splitInp[1])
                    return [lineCount,action,actionTime]
                else:
                    return [lineCount,action,0]

        fileHandle.close()
        return [lineCount,-1]

    def getNestInput(self):
        if (os.path.isfile("actions.txt")):
            fileHandle = open("actions.txt",'r')
            newInput = self.getNewNestInput(fileHandle)
            print newInput
            if (self.nestInputLines == 0):
                self.toSpinQ.setTicks(0)
                self.nestInputLines = 1
                print 'turn step environment started'
            if (newInput[0] > self.nestInputLines):
                self.nestInputLines = newInput[0]
                action = newInput[1]
                #print 'new input',newInput
                print 'new input',self.nestInputLines,newInput[1]
                print 'act on', newInput[1], ' ', newInput[2]
                self.toSpinQ.setTicks(newInput[2])
                self.processCommandFromBoard(action)
        self.toSpinQ.increaseTimeTicks()
        self.toSpinQ.sendWord()
        self.after(200,self.getNestInput)

    #gets the input from the text box and write the sentence
    def processTextInput (self, textInput):
        #clear whitespace before and after
        input = textInput.rstrip()
        input = input.lstrip()
        input = input.lower()

        if input == "add bulb":
            self.toSpinQ.writeSentence([-1,0,1,2],4)
        elif input == "add fan":
            self.toSpinQ.writeSentence([-1,0,3,2],4)
        elif input == "add music":
            self.toSpinQ.writeSentence([-1,0,4,2],4)
        elif input == "add tv":
            self.toSpinQ.writeSentence([-1,0,5,2],4)
        elif input == "add thermo":
            self.toSpinQ.writeSentence([-1,0,6,2],4)
        elif input == "turn on bulb":
            self.toSpinQ.writeSentence([-1,7,8,1,2],5)
        elif input == "turn on fan":
            self.toSpinQ.writeSentence([-1,7,8,3,2],5)
        elif input == "turn on tv":
            self.toSpinQ.writeSentence([-1,7,8,5,2],5)
        elif input == "turn on music":
            self.toSpinQ.writeSentence([-1,7,8,4,2],5)
        elif input == "turn off bulb":
            self.toSpinQ.writeSentence([-1,7,9,1,2],5)
        elif input == "turn off fan":
            self.toSpinQ.writeSentence([-1,7,9,3,2],5)
        elif input == "turn off tv":
            self.toSpinQ.writeSentence([-1,7,9,5,2],5)
        elif input == "turn off music":
            self.toSpinQ.writeSentence([-1,7,9,4,2],5)
        elif input == "set thermo low":
            self.toSpinQ.writeSentence([-1,10,6,11,2],5)
        elif input == "set thermo mid":
            self.toSpinQ.writeSentence([-1,10,6,12,2],5)
        elif input == "set thermo high":
            self.toSpinQ.writeSentence([-1,10,6,13,2],5)
        else:
            print "bad text input", textInput


    fPrintedCommand = False
    fPrintedNoCommand = False

    #depending on the number command an action is performed.
    def processCommandFromBoard(self,commandNum):
        print 'check number' , commandNum
        if (commandNum == 0):
            self.addDevice('Bulb')
        elif (commandNum == 1):
            self.addDevice('Fan')
        elif (commandNum == 2):
            self.addDevice('Music')
        elif (commandNum == 3):
            self.addDevice('Tv')
        elif (commandNum == 4):
            self.addDevice('Thermostat')
        elif (commandNum == 5):
            self.turnOn('Bulb')
        elif (commandNum == 6):
            self.turnOn('Fan')
        elif (commandNum == 7):
            self.turnOn('Tv')
        elif (commandNum == 8):
            self.turnOn('Music')
        elif (commandNum == 9):
            self.turnOff('Bulb')
        elif (commandNum == 10):
            self.turnOff('Fan')
        elif (commandNum == 11):
            self.turnOff('Tv')
        elif (commandNum == 12):
            self.turnOff('Music')
        elif (commandNum == 13):
            self.setThermo('Low')
        elif (commandNum == 14):
            self.setThermo('Mid')
        elif (commandNum == 15):
            self.setThermo('High')
        else:
            print ("environment ignores action ", commandNum)

    #send the sentence when you hit return
    def keyHandler(self,event):
        #print "keyhandler", repr(event.char)
        if (event.char == '\r'):
            text = self.editBox.get(1.0,END)
            self.editBox.delete(1.0,END)
            self.processTextInput(text)
            #self.putTextInFile(text)

    #function to update the gui and check if the device has already been added
    def addDevice(self,deviceName):
        children = self.treeview.get_children('')
        check = False
        for child in children:
            values = self.treeview.item(child,'text')
            if deviceName in values:
                check = True
        if check == False:
            if deviceName == 'Thermostat':
                self.treeview.insert('','end',text = deviceName,values=('LOW'))
            else:
                self.treeview.insert('','end',text = deviceName,values=('OFF'))
        else:
            print ("Device already exists")

    #functions to update the status of the device
    def turnOn(self,deviceName):
        children = self.treeview.get_children('')
        check = False
        for child in children:
            values = self.treeview.item(child,'text')
            if deviceName in values:
                check == True
                tempChild = child
        if check == False:
            self.treeview.delete(child)
            self.treeview.insert('','end',text = deviceName,values=('ON'))
        else:
            print("Device does not exist")

    def turnOff(self,deviceName):
        children = self.treeview.get_children('')
        check = False
        for child in children:
            values = self.treeview.item(child,'text')
            if deviceName in values:
                check == True
                tempChild = child
        if check == False:
            self.treeview.delete(tempChild)
            self.treeview.insert('','end',text = deviceName,values=('OFF'))
        else:
            print("Device does not exist")

    def setThermo(self,levelName):
        children = self.treeview.get_children('')
        check = False
        for child in children:
            values = self.treeview.item(child,'text')
            if "Thermostat" in values:
                check == True
                tempChild = child
        if check == False:
            self.treeview.delete(tempChild)
            self.treeview.insert('','end',text = "Thermostat",values=(levelName))
        else:
            print("Device does not exist")
        # print 0
    #set up the tickle frame with and edit box, buttons
    def initUI(self):
        self.parent.title("Turn Step Environment")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)

        self.canvas.pack(fill=BOTH, expand=1)

        #quit button
        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=0, y=0)

        #edit box to take inputs
        self.editBox = Text(self,height=1, width=50)
        self.editBox.place(x=0, y=25)
        self.editBox.bind("<Key>",self.keyHandler)

        #table to show device name and status
        tv = Treeview(self)
        tv['columns'] = ('status')
        tv.heading("#0",text='Widget', anchor='w')
        tv.column('#0',anchor='w')
        tv.heading('status', text='Status')
        tv.column('status',anchor='center',width=100)
        # tv.grid(sticky=(N,S,W,E))
        self.treeview = tv
        self.treeview.place(x=0,y=50)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    #end of class

def main():
    print "main"
    root = Tk()
    env = Environment(root)
    root.geometry("500x200+300+300")
    root.mainloop()


if __name__ == '__main__':
    main()
