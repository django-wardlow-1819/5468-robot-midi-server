import NetworkTablesWrapper
import MidiInterfaceWrapper
import StupidDumbGuiWrapperGarbage
import threading


class Main:
    tables = None
    midi = None
    gui = None
    run = True

    def __init__(self):
        self.intiGui()

    def intiGui(self):
        self.gui = StupidDumbGuiWrapperGarbage.TkinterBad(lambda a, b, c: self.start(a, b, c), lambda: self.stop())

    def stop(self):
        self.run = False
        self.tables.stop()

    def start(self, ip, ins, out):
        self.midi = MidiInterfaceWrapper.MidiWrapper(
            ins, out, lambda a, b: self.tables.update_note(a, b),
            lambda a, b: self.tables.update_cc(a, b))

        self.tables = NetworkTablesWrapper.NetworkTableWrapper(
            ip,
            lambda c: self.conected(c),
            lambda id, value: self.midi.send_cc(id, value),
            lambda id, value: self.midi.send_NoteOn(id, value)
        )

        threading.Thread(target=self.colect).start()

    def colect(self):
        while self.run:
            self.midi.collect_data()

    def conected(self, c):
        self.gui.setConected(c)


x = Main()
