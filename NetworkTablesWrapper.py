import threading
from networktables import NetworkTablesInstance
import time


class NetworkTableWrapper:
    connected = False
    # all tables
    tables = NetworkTablesInstance()
    # fake so autofill still works
    ccTable = tables.getTable("fake")
    noteTable = tables.getTable("fake")
    Return = tables.getTable("fake")
    receiveAction = None
    receivers = []
    conectedAction = None

    # magic copied code to make network tables start
    def __init__(self, ip, conectedAction, reciveAction):
        self.connected = False
        self.conectedAction = conectedAction
        self.receiveAction = reciveAction
        cond = threading.Condition()
        notified = [False]

        def connection_listener(connected, info):
            self.connected = connected
            self.ccTable = self.tables.getTable("ccTable")
            self.noteTable = self.tables.getTable("noteTable")
            self.Return = self.tables.getTable("Return")
            with cond:
                notified[0] = True
                cond.notify()
            self.create_receivers()
            self.create_received_listeners()
            self.conectedAction(connected)

        self.tables.initialize(server=ip)
        self.tables.setUpdateRate(0.01)
        self.tables.addConnectionListener(connection_listener, immediateNotify=True)

        with cond:
            if not notified[0]:
                cond.wait()

    # actually runs the action
    def update_on_receive(self, key, value):
        # in python, the keys are paths so we need to take off all the garbage
        k = str(key).split("/")
        id_ = k[2]
        self.receiveAction(int(id_), value)

    # creates a array of receivers to receive updates
    def create_receivers(self):
        for x in range(128):
            self.receivers.append(self.Return.getEntry(str(x)))

    # adds listeners to the receivers that run the action on change
    def create_received_listeners(self):
        for x in self.receivers:
            x.addListener(lambda a, b, c, d: self.update_on_receive(b, c), 20)

    # sends a updated note to the robot
    def update_note(self, note, value):
        self.noteTable.putBoolean(str(note), value)

    # sends a updated cc to the robot
    def update_cc(self, cc, value):
        self.ccTable.putNumber(str(cc), value)

    def stop(self):
        self.tables.stopClient()
