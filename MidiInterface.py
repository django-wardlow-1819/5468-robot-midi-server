import rtmidi


class MidiInterface:
    inp = rtmidi.MidiIn()
    out = rtmidi.MidiOut()

    # TODO make this a enum
    commandTypes = {
        8: "NoteOff",
        9: "NoteOn",
        10: "Aftertouch",
        11: "CC",
        12: "PC",
        13: "Aftertouch Channel",
        14: "Pitch",
        15: "Sysex",
        "NoteOff": 8,
        "NoteOn": 9,
        "Aftertouch": 10,
        "CC": 11,
        "PC": 12,
        "Aftertouch Channel": 13,
        "Pitch": 14,
        "Sysex": 15
    }

    def __init__(self, inId, outid):
        self.inp.open_port(inId)
        self.out.open_port(outid)

    @staticmethod
    def getMidiDevicesString():
        return "outputs: " + str(MidiInterface.out.get_ports()) + " inputs: " + str(MidiInterface.inp.get_ports())

    @staticmethod
    def getMidiOutDevices():
        return MidiInterface.out.get_ports()

    @staticmethod
    def getMidiInDevices():
        return MidiInterface.inp.get_ports()

    # gets the midi data from the device and makes it good
    def getData(self):
        # gets data from input
        x = self.inp.get_message()
        try:
            mesage = x[0]
            # bitshifting stuff to decode the chanle from the datatype
            ch = (mesage[0] & 0b00001111) + 1
            type = MidiInterface.commandTypes.get((mesage[0] >> 4))
            # returns the chanel, then the data type then
            return [ch, type, mesage[1], mesage[2]]

        # if the midi data is bad then return none
        except:
            return None

    # gets raw data for debuging
    def getRawData(self):
        return self.inp.get_message()

    # sends a pice of data
    def sendData(self, chanle, type, byte2, byte3):
        # puts the chanle and type into the same int to send
        dataType = (MidiInterface.commandTypes.get(type) << 4)
        byte1 = (dataType | chanle - 1)
        self.out.send_message([byte1, byte2, byte3])

    # sends raw data for sysex messages
    def sendRawData(self, intArray):
        self.out.send_message(intArray)

    # for testing the midi conections
    def test(self):
        print(self.inp.get_current_api())
        print(self.inp.is_port_open())
