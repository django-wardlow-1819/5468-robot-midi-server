import threading
import MidiInterface

class MidiWraper:
    chanle = 1
    stop = False
    midi = None
    midiCCs = []
    oldMidiCCs = []
    midiNotes = []
    colectionThred = None

    def __init__(self, inPort, outPort, ):
        midi = MidiInterface.MidiInterface(inPort, outPort)
        self.colectionThred = threading.Thread(target=self.colectData)
        self.initArrays()
        self.midi = midi

    def startMidiColection(self):
        self.stop = False
        self.colectionThred.start()

    def colectData(self):
        while True:
            #checks the arrays atleast once then when data is present beak and change arrays acordingly
            data = None
            while data is None:
                #checks tyo see if it should stop
                if self.stop:
                    break
                self.checkArrays()
                data = self.midi.getData()

            #auctly stops
            if self.stop:
                break

            #changes note array on note commands
            if data[1] == "NoteOn":
                self.midiNotes[data[2]] = True
            if data[1] == "NoteOff":
                self.midiNotes[data[2]] = False

            #changes cc array on new cc
            if data[1] == "CC":
                self.midiCCs[data[2]] = data[3]

    # runs through arrays and changes all values in old array to match new one and sends the new values to the sliders
    def checkArrays(self):
        for x in range(128):
            if self.midiCCs[x] != self.oldMidiCCs[x]:
                self.changeSlider(x, self.midiCCs[x])
                self.oldMidiCCs[x] = self.midiCCs[x]

    #changes a slider
    def changeSlider(self, slider, value):
        self.midi.sendData(self.chanle, "CC", slider, value)

    def SendRawData(self, array):
        self.midi.sendRawData(array)

    def StopMidiColection(self):
        self.stop = True
        while self.colectionThred.is_alive():
            pass

    def initArrays(self):
        for x in range(128):
            self.midiCCs.append(0)
        for x in range(128):
            self.oldMidiCCs.append(0)
        for x in range(128):
            self.midiNotes.append(False)
