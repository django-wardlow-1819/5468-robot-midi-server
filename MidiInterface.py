import rtmidi
from rtmidi.midiutil import open_midiinput


class MidiInterface:
    inp = rtmidi.MidiIn()
    out = rtmidi.MidiOut()

    commandTypes = {
        8: "NoteOff",
        9: "NoteOn",
        10: "Aftertouch",
        11: "CC",
        12: "PC",
        13: "Aftertouch Channel",
        14: "Pitch",
        15: "Sysex"
    }

    def __init__(self, inId, outid):
        self.inp.open_port(inId)
        self.out.open_port(outid)

    @staticmethod
    def getMidiDevices():
        return "outputs: " + str(MidiInterface.out.get_ports()) + " inputs: " + str(MidiInterface.inp.get_ports())

    def getData(self):
        x = self.inp.get_message()
        try:

            mesage = x[0]
            ch = (mesage[0] & 0b00001111) + 1
            type = MidiInterface.commandTypes.get((mesage[0] >> 4))
            # returns the chanel, then the data type then
            return [ch, type, mesage[1], mesage[2]]

        # if the midi data is bad then return none
        except:
            return None

    def getRawData(self):
        return self.inp.get_message()

    def sendRawData(self, chanle, byte2, byte3):
        self.out.send_message([chanle + 143, byte2, byte3])

    def test(self):
        print(self.inp.get_current_api())
        print(self.inp.is_port_open())
