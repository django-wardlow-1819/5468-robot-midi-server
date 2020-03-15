import threading
import MidiInterface

class MidiWraper:
    stop = False
    midi = None
    midiCCs = []
    oldMidiCCs = []
    colectionThred = None

    def __init__(self, midi):
        self.colectionThred = threading.Thread(target=self.colectData)
        self.initArrays()
        self.midi = midi

    def StartMidiColection(self):
        self.stop = False
        self.colectionThred.start()

    def colectData(self):
        while True:
            if self.stop:
                break
            #colect data and put it into the array

    def StopMidiColection(self):
        self.stop = True
        while self.colectionThred.is_alive():
            pass


    def initArrays(self):
        for x in range(128):
            self.midiCCs.append(0)
        for x in range(128):
            self.oldMidiCCs.append(0)
