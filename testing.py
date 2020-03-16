import MidiInterfaceWrapper
import time
import random

#print(MidiInterface.MidiInterface.getMidiDevices())

midi = MidiInterfaceWrapper.MidiWraper(2, 3)
print(midi.getDevices())
midi.startMidiColection()

while True:
    print(midi.midiCCs)
    time.sleep(2)
    #midi.midiCCs[1] = random.randint(0,127)
