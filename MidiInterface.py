import rtmidi
from rtmidi.midiutil import open_midiinput

class MidiInterface:
    inp = rtmidi.MidiIn()
    out = rtmidi.MidiOut()

    def __init__(self, inId, outid):
        self.inp.open_port(inId)
        #self.out.open_port(outid)

    @staticmethod
    def getMidiDevices():
        return "outputs: "+str(MidiInterface.out.get_ports())+" inputs: "+str(MidiInterface.inp.get_ports())

    def getRawData(self):
        return self.inp.get_message()

    def test(self):
        print(self.inp.get_current_api())
        print(self.inp.is_port_open())