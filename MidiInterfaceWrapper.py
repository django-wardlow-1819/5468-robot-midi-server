import MidiInterface


class MidiWrapper:
    # midi channel to send on
    channel = 1
    midi = None
    # things to do when cc or note received
    noteAction = None
    ccAction = None

    # cc and note action require a id(0-127) and a value (cc(0-127), note(True/False))
    def __init__(self, in_port, out_port, note_action, cc_action):
        self.midi = MidiInterface.MidiInterface(in_port, out_port)
        self.noteAction = note_action
        self.ccAction = cc_action

    def collect_data(self):
        # gets data from interface
        data = self.midi.get_data()
        # returns if no data
        if data is None:
            return
        # runs note command on note recive
        if data[1] == "NoteOn":
            self.noteAction(data[2], True)
        if data[1] == "NoteOff":
            self.noteAction(data[2], False)

        # runs cc_action on cc receive
        if data[1] == "CC":
            self.ccAction(data[2], data[3])

    # sends a cc
    def send_cc(self, id, value):
        self.midi.send_data(self.channel, "CC", id, value)

    # sends a noteOn
    def send_NoteOn(self, id, value):
        self.midi.send_data(self.channel, "NoteOn", id, value)

    # sends raw data to midi devices for sysex
    def send_raw_data(self, array):
        self.midi.send_raw_data(array)

    # TODO impliment
    def send_string(self):
        raise Exception("NOT IMPLEMENTED!")

    @staticmethod
    def getInputs():
        return MidiInterface.MidiInterface.get_midi_in_devices()

    @staticmethod
    def getOutputs():
        return MidiInterface.MidiInterface.get_midi_out_devices()

    @staticmethod
    def get_devices():
        return MidiInterface.MidiInterface.get_midi_devices_string()
