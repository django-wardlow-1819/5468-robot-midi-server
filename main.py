import tkinter
import threading
from pygame import midi
midi.init()

import threading
from networktables import NetworkTables

cond = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)
    with cond:
        notified[0] = True
        cond.notify()

NetworkTables.initialize(server='127.0.0.1')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

with cond:
    print("Waiting")
    if not notified[0]:
        cond.wait()

while True:
    table = NetworkTables.getTable("midi")
    print(table.getNumber('a',0))
    exit()

