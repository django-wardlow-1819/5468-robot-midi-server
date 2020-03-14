import MidiInterface



print(MidiInterface.MidiInterface.getMidiDevices())

midi = MidiInterface.MidiInterface(0, 1)

#midi.sendRawData(16, )

while True:
    x = midi.getData()
    if(x != None):
        print(x)