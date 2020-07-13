import NetworkTablesWrapper
import MidiInterfaceWrapper
import GUI
import threading


class Main:
    tables = None
    midi = None
    gui = None
    run = True

    # TODO all the lambdas everywhere are DUMB

    # creats the gui when program started
    def __init__(self):
        self.gui = GUI.makeGUI(lambda a, b, c: self.start(a, b, c), lambda: self.stop())

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

    # runs as a thred and colects+prosses any new midi data
    def colect(self):
        while self.run:
            self.midi.collect_data()


# inits the main class
x = Main()
