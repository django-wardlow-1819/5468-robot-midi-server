import MidiInterface


class MidiWraper:
    # midi chanle to send on
    chanle = 1
    midi = None
    # things to do when cc or note recived
    noteAction = None
    ccAction = None

    # cc and note action require a id(0-127) and a value (cc(0-127), note(True/False))
    def __init__(self, inPort, outPort, noteAction, ccAction):
        self.midi = MidiInterface.MidiInterface(inPort, outPort)
        self.noteAction = noteAction
        self.ccAction = ccAction

    def colectData(self):
        # gets data from interface
        data = self.midi.getData()
        # returns if no data
        if data is None:
            return
        # runs note command on note recive
        if data[1] == "NoteOn":
            self.noteAction(data[2], True)
        if data[1] == "NoteOff":
            self.noteAction(data[2], False)

        # runs ccAction on cc recive
        if data[1] == "CC":
            self.ccAction(data[2], data[3])

    # changes a slider on vertualsliders
    # TODO mkae this work with whatever conteroler we end up using
    def changeSlider(self, slider, value):
        self.midi.sendData(self.chanle, "CC", slider, value)

    # sends raw data to midi devices for sysex
    def SendRawData(self, array):
        self.midi.sendRawData(array)

    # TODO impliment
    def sendString(self):
        raise Exception("NOT IMPLIMENTED!")

    @staticmethod
    def getDevices():
        return MidiInterface.MidiInterface.getMidiDevicesString()
