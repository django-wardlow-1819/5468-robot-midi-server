import NetworkTablesWrapper
import MidiInterfaceWrapper

print(MidiInterfaceWrapper.MidiWrapper.get_devices())
tables = NetworkTablesWrapper.NetworkTableWrapper('127.0.0.1')
midi = MidiInterfaceWrapper.MidiWrapper(
    0, 2, lambda a, b: tables.update_note(a, b),
    lambda a, b: tables.update_cc(a, b))

tables.set_update_action(lambda id_, value: midi.change_slider(id_, value))

while True:
    midi.collect_data()
