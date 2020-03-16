import MidiInterfaceWrapper
import time
import random

#print(MidiInterface.MidiInterface.getMidiDevices())

midi = MidiInterfaceWrapper.MidiWrapper(2, 3)
print(midi.get_devices())
midi.startMidiColection()

while True:
    print(midi.midiCCs)
    time.sleep(2)
    #midi.midiCCs[1] = random.randint(0,127)
