import rtmidi


class MidiInterface:
    inp = rtmidi.MidiIn()
    out = rtmidi.MidiOut()

    # TODO make this not bad
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

    # open input and output when class initlised
    def __init__(self, in_id, out_id):
        self.inp.open_port(in_id)
        self.out.open_port(out_id)

    @staticmethod
    def get_midi_devices_string():
        return "outputs: " + str(MidiInterface.out.get_ports()) + " inputs: " + str(MidiInterface.inp.get_ports())

    @staticmethod
    def get_midi_out_devices():
        return MidiInterface.out.get_ports()

    @staticmethod
    def get_midi_in_devices():
        return MidiInterface.inp.get_ports()

    # gets the midi data from the device and makes it good
    def get_data(self):
        # gets data from input
        x = self.inp.get_message()
        try:
            message = x[0]
            # bit shifting stuff to separate the channel from the data type
            ch = (message[0] & 0b00001111) + 1
            midi_type = MidiInterface.commandTypes.get((message[0] >> 4))
            # returns the chanel, then the data type then the message bytes
            return [ch, midi_type, message[1], message[2]]

        # if the midi data is bad then return none
        except Exception:
            return None

    # gets raw data for debugging
    def get_raw_data(self):
        return self.inp.get_message()

    # sends a piece of data
    def send_data(self, channel, type_, byte2, byte3):
        # puts the channel and type into the same int to send
        data_type = (MidiInterface.commandTypes.get(type_) << 4)
        byte1 = (data_type | channel - 1)
        self.out.send_message([byte1, byte2, byte3])

    # sends raw data for sysex messages
    def send_raw_data(self, int_array):
        self.out.send_message(int_array)

    # for testing the midi connections
    def test(self):
        print(self.inp.get_current_api())
        print(self.inp.is_port_open())
