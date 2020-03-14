import MidiInterface

midi = MidiInterface.MidiInterface(0, 0)

print(midi.getMidiDevices())

#midi.test()

while True:
    x = midi.getRawData()
    if(x != None):
        print(x)