import MidiWraper
import time
import random

#print(MidiInterface.MidiInterface.getMidiDevices())

midi = MidiWraper.MidiWraper(0,2)

midi.startMidiColection()

while True:
    print(midi.midiCCs)
    time.sleep(2)
    midi.midiCCs[1] = random.randint(0,127)