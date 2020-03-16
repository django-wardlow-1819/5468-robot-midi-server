import NetworrkTablesWrapper
import MidiInterfaceWrapper

print(MidiInterfaceWrapper.MidiWraper.getDevices())
tables = NetworrkTablesWrapper.NetwarkTableWraper('127.0.0.1')
midi = MidiInterfaceWrapper.MidiWraper(0, 2, lambda a, b: tables.updateNote(a, b), lambda a, b: tables.updateCC(a, b))

tables.setUpdateAction(lambda id, value: midi.changeSlider(id, value))

while True:
    midi.colectData()
