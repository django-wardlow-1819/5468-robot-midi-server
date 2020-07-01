import NetworkTablesWrapper
import MidiInterfaceWrapper
import StupidDumbGuiWrapperGarbage
import threading


class Main:
    tables = None
    midi = None
    gui = None
    run = True

    # creats the gui when class initlised
    def __init__(self):
        self.gui = StupidDumbGuiWrapperGarbage.TkinterBad(lambda a, b, c: self.start(a, b, c), lambda: self.stop())

    # stops midi colection and netowrktables
    def stop(self):
        self.run = False
        # so you can close when tables havent started
        try:
            self.tables.stop()
        except:
            pass

    # starts midi and networktables client
    def start(self, ip, ins, out):
        # args are in_port, out_port, note_action, cc_action
        self.midi = MidiInterfaceWrapper.MidiWrapper(
            ins,
            out,
            lambda a, b: self.tables.update_note(a, b),
            lambda a, b: self.tables.update_cc(a, b)
        )

        # args are ip, conectedAction, CCreciveAction, NoteReciveAction
        self.tables = NetworkTablesWrapper.NetworkTableWrapper(
            ip,
            lambda c: self.gui.setConected(c),
            lambda id, value: self.midi.send_cc(id, value),
            lambda id, value: self.midi.send_NoteOn(id, value)
        )

        threading.Thread(target=self.colect).start()

    # runs as a thred and colects the midi data
    def colect(self):
        while self.run:
            self.midi.collect_data()


x = Main()
