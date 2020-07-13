import threading
from networktables import NetworkTablesInstance


# DONT TOUCH UNLESS BROKEN
class NetworkTableWrapper:
    connected = False
    made = True
    # all tables
    tables = NetworkTablesInstance()
    ccTable = None
    noteTable = None
    CCReturn = None
    NoteReturn = None
    CCreceiveAction = None
    NoteReceiveAction = None
    CCreceivers = []
    NoteReceivers = []
    conectedAction = None

    # magic copied code to make network tables start
    def __init__(self, ip, conectedAction, CCreciveAction, NoteReciveAction):
        self.connected = False
        self.conectedAction = conectedAction
        self.CCreceiveAction = CCreciveAction
        self.NoteReceiveAction = NoteReciveAction
        cond = threading.Condition()
        notified = [False]

        def connection_listener(connected, info):
            print(info)
            self.connected = connected
            self.ccTable = self.tables.getTable("ccTable")
            self.noteTable = self.tables.getTable("noteTable")
            self.CCReturn = self.tables.getTable("CCReturn")
            self.NoteReturn = self.tables.getTable("NoteReturn")
            with cond:
                notified[0] = True
                cond.notify()
            # to prevent runing agin if robot disconects and reconects
            if self.made:
                self.create_receivers()
                self.create_received_listeners()
                self.made = False
            self.conectedAction(connected)

        self.tables.startClient(ip)
        self.tables.setUpdateRate(0.01)
        self.tables.addConnectionListener(connection_listener, immediateNotify=True)

        with cond:
            if not notified[0]:
                cond.wait()

    # actually runs the action
    def update_on_cc_receive(self, key, value):
        # in python, but not java, the keys are formated like paths so we need to take off all the garbage
        k = str(key).split("/")
        id_ = k[2]
        self.CCreceiveAction(int(id_), value)

    def update_on_note_receive(self, key, value):
        # in python, but not java, the keys are formated like paths so we need to take off all the garbage
        k = str(key).split("/")
        id_ = k[2]
        self.NoteReceiveAction(int(id_), value)

    # creates a array of receivers to receive MIDI updates from networktables
    def create_receivers(self):
        for x in range(128):
            self.CCreceivers.append(self.CCReturn.getEntry(str(x)))
            self.NoteReceivers.append(self.NoteReturn.getEntry(str(x)))

    # adds listeners to the receivers that run the action on change
    def create_received_listeners(self):
        for x in self.CCreceivers:
            x.addListener(lambda a, b, c, d: self.update_on_cc_receive(b, c), 20)
        for x in self.NoteReceivers:
            x.addListener(lambda a, b, c, d: self.update_on_note_receive(b, c), 20)

    # sends a updated note to the robot
    def update_note(self, note, value):
        self.noteTable.putBoolean(str(note), value)

    # sends a updated cc to the robot
    def update_cc(self, cc, value):
        self.ccTable.putNumber(str(cc), value)

    # stops networktables
    def stop(self):
        self.tables.stopClient()
