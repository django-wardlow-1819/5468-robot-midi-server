import MidiInterface



print(MidiInterface.MidiInterface.getMidiDevices())

midi = MidiInterface.MidiInterface(0, 2)

midi.sendData(1, "CC", 1, 127)

while True:
    x = midi.getData()
    if x != None:
        print(x)